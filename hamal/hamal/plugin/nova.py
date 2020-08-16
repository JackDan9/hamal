# Copyright 2020 Hamal, Inc.

from oslo_log import log as logging

from hamal.exception import HamalException
from hamal.utils.plugin import get_request, post_request, delete_request
from hamal.i18n import _, _LE


LOG = logging.getLogger(__name__)

INSTANCES_URL = '/servers/detail'
INSTANCE_URL = '/servers/{instance_id}'
INSTANCE_ACTION_URL = '/servers/{instance_id}/action'
INSTANCE_VOLUME_ATTACHMENTS_URL = '/servers/{instance_id}/os-volume_attachments'
INSTANCE_INTERFACE_URL = '/servers/{instance_id}/os-interface'

FLAVORS_URL = '/flavors'
FLAVOR_URL = '/flavors/{flavor_id}'

VOLUME_BOOT_URL = '/os-volumes_boot'

IMAGE_URL = '/images/{image_id}'


class InterfacePlugin(object):
    """A plugin of Interface"""
    
    def get_instance(self, instance_id):
        pass


class NovaPlugin(object):
    """A plugin of Nova"""

    def __init__(self, host_url, openstack):
        self.host_url = host_url
        self.openstack = openstack
        self._instance_url = self.host_url + INSTANCE_URL
        self._instances_url = self.host_url + INSTANCES_URL
        self._instance_action_url = self.host_url + INSTANCE_ACTION_URL
        self._instance_volume_attachments_url = self.host_url + INSTANCE_VOLUME_ATTACHMENTS_URL
        self._instance_interface_url = self.host_url + INSTANCE_INTERFACE_URL
        self._flavors_url = self.host_url + FLAVORS_URL
        self._flavor_url = self.host_url + FLAVOR_URL
        self._volume_boot_url = self.host_url + VOLUME_BOOT_URL
        self._image_url = self.host_url + IMAGE_URL
    
    @property
    def openstack_user_token(self):
        return self.openstack.openstack_user_token
    
    def get_list_instance(self):
        return get_request(self._instances_url, self.openstack_user_token)
    
    def get_instance(self, instance_id):
        instance_url = self._instance_url.format(instance_id=instance_id)
        return get_request(instance_url, self.openstack_user_token)

    def delete_instance(self, instance_id):
        instance_url = self._instance_url.format(instance_id=instance_id)
        return delete_request(instance_url, self.openstack_user_token)

    def stop_instance(self, instance_id):
        instance_url = self._instance_action_url.format(instance_id=instance_id)
        data = {
            "os-stop": None
        }
        
        try:
            return post_request(instance_url, body=data, token=self.openstack_user_token, no_resp_content=True)
        except HamalException as he:
            LOG.exception(_LE("Stop instance exception is : %(he)s", 
                          {"he": he}))
            if he.code != 409:
                raise he
    
    def start_instance(self, instance_id):
        instance_url = self._instance_action_url.format(instance_id=instance_id)
        data = {
            "os-start": None
        }
        try:
            return post_request(instance_url, body=data, token=self.openstack_user_token, no_resp_content=True)
        except HamalException as he:
            LOG.exception(_LE("Start instance exception is : %(he)s", 
                              {"he": he}))
            if he.code != 409:
                raise he
        
    def volumes_boot(self, name, flavor_id, source_type, source_id, volume_size, net_ids):
        volume_boot_url = self._volume_boot_url

        data = {
            "server": {
                "name": name,
                "imageRef": "",
                "block_device_mapping_v2": [
                    {
                        "boot_index": "0",
                        "uuid": source_id,
                        "volume_size": volume_size,
                        "device_name": "vda",
                        "source_type": source_type,
                        "device_type": "disk",
                        "destination_type": "volume"
                    }
                ],
                "flavorRef": flavor_id,
                "max_count": 1,
                "min_count": 1,
                "networks": map(lambda net_id: {"uuid": net_id}, net_ids)
            }
        }

        resp_data = post_request(volume_boot_url, data, self.openstack_user_token)
        return resp_data
    
    def volume_attach_instance(self, instance_id, volume_id):
        instance_volume_attachment_url = self._instance_volume_attachments_url.format(instance_id=instance_id)
        
        data = {
            "volumeAttachment": {
                "device": None,
                "volumeId": volume_id
            }
        }

        return post_request(instance_volume_attachment_url, data, self.openstack_user_token)

    def get_flavor(self, flavor_id):
        flavor_url = self._flavor_url.format(flavor_id=flavor_id)
        return get_request(flavor_url, self.openstack_user_token)

    def list_flavor(self):
        return get_request(self._flavors_url, self.openstack_user_token)

    def create_flavor(self, vcpus, disk, name, is_public, rxtx_factor, ephemeral, ram, swap):
        data = {
            "flavor": {
                "vcpus": vcpus,
                "disk": disk,
                "name": name,
                "os-flavor-access:is_public": is_public,
                "rxtx_factor": rxtx_factor,
                "OS-FLV-EXT-DATA:ephemeral": ephemeral,
                "ram": ram,
                "id": None,
                "swap": swap
            }
        }

        resp_data = post_request(self._flavors_url, data, self.openstack_user_token)
        return resp_data
    
    def delete_flavor(self, flavor_id):
        flavor_url = self._flavor_url.format(flavor_id=flavor_id)
        return delete_request(flavor_url, self.openstack_user_token)

    def get_image(self, image_id):
        image_url = self._image_url.format(image_id=image_id)
        return get_request(image_url, self.openstack_user_token)

    def delete_image(self, image_id):
        image_url = self._image_url.format(image_id=image_id)
        return delete_request(image_url, self.openstack_user_token)

    def get_instance_interface(self, instance_id):
        instance_interface_url = self._instance_interface_url.format(instance_id=instance_id)
        return get_request(instance_interface_url, self.openstack_user_token)
