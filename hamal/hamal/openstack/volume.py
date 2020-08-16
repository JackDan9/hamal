# Copyright 2020 Hamal, Inc.

from oslo_log import log as logging

from hamal.openstack.base import DataBase
from hamal.openstack.base import SourceBase
from hamal.openstack.common import Wait
from hamal.db import api as db_api
from hamal.i18n import _, _LE
import hamal.conf


CONF = hamal.conf.CONF


LOG = logging.getLogger(__name__)


class VolumeData(DataBase):
    """The class of volume data"""

    def __init__(self, data):
        self.data = data['volume']
    
    @property
    def image_disk_format(self):
        return self.data.get('volume_image_metadata', {}).get('disk_format')
    
    @property
    def image_container_format(self):
        return self.data.get('volume_image_metadata', {}).get('container_format')
    

class VolumeDoingLock(object):
    """The class of volume doing lock"""

    def __init__(self, volume):
        self.volume = volume
    
    def __enter__(self):
        self.volume.set_status('in_use')
        return self
    
    def __exit__(self, *exc_info):
        self.volume.set_status('available')
    

class Volume(SourceBase):
    """The class of volume"""

    def __init__(self, plugin, source_id):
        super(Volume, self).__init__(plugin, source_id)
        self._volume_obj = None
    
    def volume_doing_lock(self):
        return VolumeDoingLock(self)

    @staticmethod
    def get(plugin, source_id):
        volume = Volume(plugin, source_id)
        plugin.cinder.get_volume(source_id)
        return volume
    
    @staticmethod
    def create(plugin, volume_size, display_name, display_description, volume_type=None):
        resp_data = plugin.cinder.create_volume(volume_size, display_name, display_description, volume_type=volume_type)
        return Volume(plugin, resp_data['volume']['id'])

    @property
    def volume_obj(self):
        if self._volume_obj is not None:
            return self._volume_obj
        self._volume_obj = VolumeData(self.show())
        return self._volume_obj

    def is_created(self):
        info = self.show()
        status = info['volume']['status']
        if status in ('created', ):
            return True
        return False

    def is_available(self):
        info = self.show()
        status = info['volume']['status']
        if status in ('available', ):
            return True
        return False

    def is_inuse(self):
        info = self.show()
        status = info['volume']['status']
        if status in ('in-use', ):
            return True
        return False 

    def show(self):
        return self.plugin.cinder.get_volume(self.id)

    def delete(self):
        return self.plugin.cinder.delete_volume(self.id)
    
    def create_instance(self, name, flavor_id, volume_size, net_ids):
        pass