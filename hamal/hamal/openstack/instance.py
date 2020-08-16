# Copyright 2020 Hamal, Inc.

from oslo_log import log as logging

from hamal.exception import HamalException
from hamal.exception import TimeoutHttpException
from hamal.openstack.base import DataBase
from hamal.openstack.base import SourceBase
from hamal.openstack.common import Wait

from hamal.openstack.volume import Volume
# from hamal.openstack.flavor import Flavor
# from hamal.openstack.port import Port
from hamal.i18n import _, _LE, _LI


LOG = logging.getLogger(__name__)


class InstanceData(DataBase):
    """The class of instance data"""

    def __init__(self, plugin, data):
        self.plugin = plugin
        self.data = data

    @property
    def volumes(self):
        volume_ids = map(lambda volume: volume['id'], self.data['os-extended-volumes:volumes_attached'])
        return [Volume(self.plugin, volume_id) for volume_id in volume_ids]

    # @property
    # def flavor(self):
    #     flavor_id = self.data['flavor_id']
    #     return Flavor(self.plugin, flavor_id)
    
    @property
    def task_state(self):
        return self.data['OS-EXT-STS:task_state']


class Instance(SourceBase):
    """The class of instance"""

    def __init__(self, plugin, source_id):
        super(Instance, self).__init__(plugin, source_id)
        self._instance_obj = None
    
    @staticmethod
    def get(plugin, source_id):
        instance = Instance(plugin, source_id)
        plugin.nova.get_instance(source_id)
        return instance
    
    @property
    def instance_obj(self):
        if self._instance_obj is not None:
            return self._instance_obj
        self._instance_obj = InstanceData(self.plugin, self.show())
        return self._instance_obj

    def instance_list(self):
        return self.plugin.nova.list_instance()

    def show(self):
        return self.plugin.nova.get_instance(self.id)

    def delete(self):
        self.plugin.nova.delete_instance(self.id)

    def delete_with_system_volume(self):
        volumes = self._instance_obj.volumes

        self.plugin.nova.delete_instance(self.id)

        def is_delete():
            try:
                self.show()
            except HamalException as he:
                LOG.exception(_LE('Hamal Exception with the %(he)s', {'he': he}))
                if he.code == 404:
                    return True
        
        wait = Wait(is_delete)
        wait.wait(interval=3, max_time=180)

        volumes[0].delete()
    
    def is_shutdown(self):
        content = self.show()
        instance_status = content['server']['status']

        if instance_status == 'SHUTOFF':
            return True
        return False

    def is_active(self):
        content = self.show()
        instance_status = content['server']['status']

        if instance_status == 'ACTIVE':
            return True
        return False

    def is_created(self):
        content = self.show()
        instance_status = content['server']['status']

        if instance_status in ('SHUTOFF', 'ACTIVE'):
            return True
        
        self._check_failed_status(instance_status)
        return False
    
    def start(self, until_done=False):
        self.plugin.nova.start_instance(self.id)

        if until_done:
            for i in range(3):
                try:
                    wait = Wait(self.is_active)
                    wait.wait(interval=5, max_time=180)
                    return
                except TimeoutHttpException as timeoutHttpException:
                    LOG.exception(_LE('Hamal time out http exception is %(timeoutHttpException)s', 
                                      {'timeoutHttpException': timeoutHttpException}))
                    self.plugin.nova.start_instance(self.id)
            raise TimeoutHttpException()
    
    def shutdown(self, until_done=False):
        self.plugin.nova.stop_instance(self.id)

        if until_done:
            for i in range(3):
                try:
                    wait = Wait(self.is_shutdown)
                    wait.wait(interval=5, max_time=180)
                except TimeoutHttpException as timeoutHttpException:
                    LOG.exception(_LE('Hamal time out http exception is %(timeoutHttpException)s', 
                                      {'timeoutHttpException': timeoutHttpException}))
                    self.plugin.nova.stop_instance(self.id)
            raise TimeoutHttpException()
    
    def attach_volume(self, volume):
        return self.plugin.nova.volume_attach_instance(self.id, volume.id)
    
    # def get_ports(self):
        # response_datas = self.plugin.nova.get_instance_interface(self.id)
        # return [Port(self.plugin, response_datas['port_id']) for response_data in response_datas['interfaceAttachments']]
