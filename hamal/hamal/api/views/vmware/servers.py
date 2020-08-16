# Copyright 2020 Hamal, Inc.

from __future__ import division

import base64
from oslo_log import log as logging
from pyVmomi import vim

from hamal.api.v1.vmware.driver.vsphere import vSphere
from hamal.db import api as db_api
from hamal.i18n import _, _LE, _LI, _LW, _LC


LOG = logging.getLogger(__name__)


class ViewBuilder(object):
    """The class for vmware vsphere virtual machines."""

    def __init__(self):
        super(ViewBuilder, self).__init__()
    
    def _server_detail(self, server):
        if server is None:
            return {"server": {}}
        
        # todo(jackdan): need to add driver mode of disk
        server_ref = {
            "server": {
                "name": server.get("name"),
                "template": server.get("config.template"),
                "guestFullName": server.get("guest.guestFullName"),
                "hostName": server.get("guest.hostName"),
                "ipAddress": server.get("guest.ipAddress"),
                "numCPU": server.get("config.hardware.numCPU"),
                "memoryGB": str(server.get("config.hardware.memoryMB") / 1024), # Default MB and Integer
                "diskGB": str("%.2f" % (server.get("summary.storage.committed") / 1024**3)),
                "diskNum": self._disk_number(server.get("config.hardware.device")),
                "driver": None,
                "toolsStatus": server.get("guest.toolsStatus"),
                "toolsRunningStatus": server.get("guest.toolsRunningStatus"),
                "powerState": server.get("runtime.powerState")
            }
        }

        return server_ref

    def _server_list(self, req, body):
        vc = body.get('vc')
        user = body.get('user')
        pwd = body.get('pwd')
        uri = body.get('uri')

        servers = self._list_servers_on_exsi(vc, user, pwd, uri)

        if not isinstance(servers, list):
            return servers
        
        servers_list = []
        for server in servers:
            try:
                server = self._server_detail(server)['server']
                if not server.get('template', False):
                    servers_list.append(server)
            except KeyError:
                LOG.error(_LE('Cannot get server detail'))
        
        return {"servers": servers_list}
    
    @staticmethod
    def _disk_number(disk_device):
        disk_num = 0
        for device in disk_device:
            if device.__class__.__name__ == 'vim.vm.device.VirtualDisk':
                disk_num = disk_num + 1

        return disk_num
    
    @staticmethod
    def _list_servers_on_exsi(vc, user, pwd, uri):
        """ List servers and templates on specified ESXi

        :param vc: The IP address of vcenter
        :param user: The username of vcenter
        :param pwd: The password of vcenter
        :param uri: The uri of ESXi will be searched
        :returns: dict to list
            when return is dict, the return is fault message
            of connect to vcenter or search uri.
            when return is list. the return is list of servers
            and templates.
        """
        # Ensure the uri does not start with '/'
        # and end with '/'
        if uri.startswith('/'):
            uri = uri.split('/', 1)[1]
        if uri.endswith('/'):
            uri = uri.split('/', 1)[0]
        
        uri = uri.split('/')

        with vSphere(host=vc, user=user, pwd=pwd) as vs:
            if vs.si is None:
                LOG.error(_LE("Could not connect to the specified vcenter "
                              "using specified username and password."))
                return {
                    "msg": "Could not connect to the specified vcenter "
                           "using specified username and password."
                }
            
            datacenters = vs.si.content.rootFolder.childEntity
            find_dc = False
            for dc in datacenters:
                if dc.name == uri[0]:
                    find_dc = True
                    break
            
            if not find_dc:
                LOG.error(_LE("Could not find specified datacenter %(datacenter_name)s.", 
                              {'datacenter_name': dc.name}))
                return {"msg": "Could not find specified datacenter %s." % dc.name}
            
            hosts = vs.get_container_view(dc, [vim.HostSystem])
            find_host = False
            for host in hosts:
                if host.name == uri[-1]:
                    find_host = True
                    break
            
            if not find_host:
                LOG.error(_LE("Could not find specified esxi %(host_name)s.",
                              {'host_name': host.name}))
                return {"msg": "Could not find specified esxi %s." % host.name}
            
            prop_spec = {
                "VirtualMachine": ["name", 
                                   "guest.toolsStatus", "guest.toolsRunningStatus", "guest.guestFullName", "guest.hostName", "guest.ipAddress",
                                   "runtime.powerState", 
                                   "config.template", "config.hardware.device", "config.hardware.numCPU", "config.hardware.memoryMB", 
                                   "summary.storage.committed"]
            }

            servers = vs.property_collector(host, [vim.VirtualMachine], prop_spec)
            return servers

    def _allow_server_numbers(self, req):
        """ List of server allowed for migration
        
        :param req: The request of getting allow server numbers
        """
        result_number = dict()

        hamal_license = db_api.license_get()
        license_message = self._parse_license_message(hamal_license.license)
        
        server_numbers = license_message.get('server_nums')
        used_servers = len(db_api.task_history_get_by_all_succeed())

        result_number['server_numbers'] = server_numbers
        result_number['used_servers'] = used_servers

        LOG.info(_LI("All allowed server numbers %(server_numbers)s. Used server numbers %(used_servers)s.", 
                     {'server_numbers': server_numbers, 'used_servers': used_servers}))
        return {'server_numbers': result_number}
    
    @staticmethod
    def _parse_license_message(license):
        """ Parse the license information

        :param license: The license of hamal
        """
        hamal_license = eval(base64.b64decode(license))
        message = [i.strip() for i in hamal_license.get('message', '').split(',')]
        
        message_dict = dict()
        for m in message:
            key, value = m.split(':', 1)
            message_dict[key] = value

        return message_dict
