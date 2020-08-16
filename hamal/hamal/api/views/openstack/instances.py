# Copyright 2020 Hamal, Inc.

from __future__ import division

import base64
import time
import calendar
from dateutil import tz
from datetime import datetime

from oslo_log import log as logging

from hamal.openstack.instance import Instance
from hamal.plugin.openstack import OpenstackPlugin

class ViewBuilder(object):
    """A class for openstack instances"""

    def __init__(self):
        super(ViewBuilder, self).__init__()
    
    def _instance_list(self, req, body):
        auth_url = body['auth_url']
        username = body['username']
        password = body['password']
        tenant_id = body['tenant_id'] 

        source_auth = {
            'cluster_name': 'source',
            'auth_url': auth_url,
            'username': username,
            'password': password,
            'tenant_id': tenant_id
        }

        source_plugin = OpenstackPlugin(**source_auth)

        instances = source_plugin.nova.get_list_instance()['servers']

        return {"instances": instances}
        