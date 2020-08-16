# Copyright 2020 Hamal, Inc.

import ssl

import six
from oslo_log import log as logging
from pyVim import connect
from pyVmomi import vim
from pyVmomi import vmodl

from hamal.api.v1.exceptions import vSpherePropertyNotExist
from hamal.api.v1.vmware.driver.base import BaseDriver
from hamal.api.v1.vmware.utils.service_util import build_full_traversal
from hamal.i18n import _LI, _LE


LOG = logging.getLogger(__name__)


class VMwareDriver(BaseDriver):
    """Initialize a connection to a vcenter"""

    def __init__(self, host='localhost', port=443, user='root', pwd='', **kwargs):
        self._host = host
        self._port = port
        self._user = user
        self._pwd = pwd
        self._kwargs = kwargs
        self.si = None

        if not isinstance(self._port, six.integer_types):
            try:
                self._port = int(self._port)
            except ValueError:
                LOG.error(_LI("The type of port should be integer."))
                raise ValueError("The type of port should be integer.")
    
    def connect(self):
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        # ssl_context.verify_mode = ssl.CERT_NONE
        try:
            self.si = connect.SmartConnect(
                host=self._host,
                port=self._port,
                user=self._user,
                pwd=self._pwd,
                sslContext=ssl_context,
                **self._kwargs
            )
        except ssl.SSLError:
            try:
                self.si = connect.SmartConnectNoSSL(
                    host=self._host,
                    port=self._port,
                    user=self._user,
                    pwd=self._pwd,
                    **self._kwargs
                )
            except Exception:
                LOG.Exception(_LE("Exception connect to the specified vcenter using "
                                  "specified username and password"))
        finally:
            if self.si is None:
                LOG.error(_LE("Could not connect to the specified vcenter using "
                              "specified username and password"))
    
    def disconnect(self):
        if self.si:
            connect.Disconnect(self.si)
            self.si = None
    
    def __enter__(self):
        self.connect()
        return self.si
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()


class vSphere(VMwareDriver):
    """Some base method for retrieve exsi/vms/database, etc."""

    def __init__(self, *args, **kwargs):
        super(vSphere, self).__init__(*args, **kwargs)
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    @staticmethod
    def _parse_propspec(propspec):
        """Parses property specifications

        :param propspec: The property specifications need to be parsed
        :type propspec: dict
        :returns: a sequence of 2-tuples.
            Each containing a managed object type and a list of properties
            applicable to that type

        """
        props = []
        propspec = propspec or {}
        for obj_type, obj_props in propspec.items():
            mo_type = getattr(vim, obj_type, None)
            if mo_type is None:
                raise vSpherePropertyNotExist(mo_type)
            props.append((mo_type, obj_props,))
        
        return props
    
    @staticmethod
    def _create_filter_spec(objs, props):
        """Returns filterSpec object"""

        obj_specs = []
        prop_specs = []
        traversal = build_full_traversal()
        for obj in objs:
            obj_spec = vmodl.query.PropertyCollector.ObjectSpec(obj=obj,
                                                                selectSet=traversal)
            obj_specs.append(obj_spec)
        
        for mo_type, prop_list in props:
            # param all: bool
            # Specifies whether or not all properties of the object are read.
            # If this properties is set to true, the 'pathSet' property is ignored.
            prop_spec = vmodl.query.PropertyCollector.PropertySpec(all=False,
                                                                   type=mo_type,
                                                                   pathSet=prop_list)
            prop_specs.append(prop_spec)
        filter_spec = vmodl.query.PropertyCollector.FilterSpec(objectSet=obj_specs,
                                                               propSet=prop_specs)
        
        return filter_spec
    
    def get_container_view(self, container=None, object_type=None, recursive=True):
        """Returns the container view of specified object type

        :param container: A reference to an instance of a Folder, Datacenter,
                ResourcePool or HostSystem object.
        :type container: ManagedEntity Object
        :param object_type: An optional list of managed entity types. The server 
                associates only objects of the specified types with the view.
                If you specify an empty list, the server uses all types.
        :type object_type: list
        :param recursive: When True, include only the immediate children of the 
                container instance. When False, include additional objects by 
                following paths beyond the immedidate children.
        :type recursive: Bool
        """
        if self.si is None:
            return
        
        container = container or self.si.content.rootFolder
        container_view = self.si.content.viewManager.CreateContainerView(
            container, object_type, recursive
        )
        view = container_view.view
        container_view.Destroy()
        return view
    
    def _do_property_collector(self, objs, props, max_objecs=100):
        """Really do properties collector using RetrievePropertiesEx

        :param objs: The objects will be queried
        :param props: The properties of objects will be queried
        :param max_objects: The maximum number of ObjectContent data objects that should
        be returned in a single result from RetrievePropertiesEx. The default is 100
        """
        if self.si is None:
            return
        
        pc = self.si.content.propertyCollector
        filter_spec = self._create_filter_spec(objs, props)
        options = vmodl.query.PropertyCollector.RetrieveOptions(maxObjects=max_objecs)
        result = pc.RetrievePropertiesEx([filter_spec], options)

        # Because the maximum number of objects retrieved by RetrievePropertiesEx
        # and ContinueRetrievePropertiesEx were limit to 100. So, we need ti 
        # continue retrieve properties using token

        def _continue(token=None):
            _result = pc.ContinueRetrievePropertiesEx(token)
            _token = _result.token
            _objects = _result.objects
            if _token is not None:
                _objects_ex = _continue(_token)
                _objects.extend(_objects_ex)
            return _objects
        
        if result is None:
            return []
        
        token = result.token
        objects = result.objects
        if token is not None:
            _objects = _continue(token)
            objects.extend(_objects)
        
        return objects
    
    def property_collector(self, container=None, object_type=None, property_spec=None):
        """Retrieve specified properties of  specified objects

        :param container: A reference to an instance of a Folder, Datacenter,
                ResourcePool or HostSystem object.
        :type container: ManagedEntity Object
        :param object_type: An optional list of managed entity types. The server
                associates only objects of the specified types with the view.
                If you specify an empty list, the server uses all types.
        :type object_type: List
        :param property_spec: The property specifications need to be parsed.
        :type property_spec: dict
        :return: The ObjectContent data objects which retrieved from RetrievePropertiesEx.

        :useage
            with vSphere(host='localhost', user='root', pwd='') as vs:
                container = vs.si.content.rootFolder
                object_type = [vim.Datacenter]
                prop_spec = {
                    "VirtualMachine": ["name"]
                }
                objects = vs.property_collector(container, object_type, prop_spec)
        """
        # The type of object_type must be list
        if not isinstance(object_type, list):
            object_type = [object_type]
        
        objs = self.get_container_view(container=container, object_type=object_type)
        props = self._parse_propspec(property_spec)
        result = []
        try:
            objects = self._do_property_collector(objs, props)
        except vmodl.query.InvalidProperty:
            LOG.error(_LE("Query invalid property"))
            raise
        for obj in objects:
            value = dict()
            for prop in obj.propSet:
                value[prop.name] = prop.val
            result.append(value)
        return result
