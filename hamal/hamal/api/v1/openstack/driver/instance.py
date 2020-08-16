# Copyright 2020 Hamal, Inc.

# from oslo_log import log as logging

# from hamal.exception import HamalException
# from hamal.exception import TimeoutHttpException
# from hamal.openstack.base import DataBase
# from hamal.openstack.base import SourceBase
# from hamal.openstack.common import Wait
# from hamal.i18n import _, _LE, _LC


# LOG = logging.getLogger(__name__)


# class InstanceData(DataBase):
#     """The class of instance data"""

#     def __init__(self, plugin, data):
#         self.plugin = plugin
#         self.data = data['instance']
    
#     @property
#     def volumes(self):
#         volume_ids = map(lambda volume: volume['id'], self.data['os-extended-volumes:volumes_attached'])
#         return [Volume(self.plugin, volume_id) for volume_id in volume_ids]

#     @property
#     def flavors(self):
#         flavor_id = self.data['flavor_id']
#         return Flavor(self.plugin, flavor_id)
    

