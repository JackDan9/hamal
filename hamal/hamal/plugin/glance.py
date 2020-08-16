# Copyright 2020 Hamal, Inc.

from urllib.parse import urlparse


class GlancePlugin(object):
    """A class for glance plugin"""

    def __init__(self, host_url, openstack):
        self.host_url = host_url
        self.openstack = openstack
        host_urlparse = urlparse(host_url)
        self.hostname = host_urlparse.hostname
        self.port = host_urlparse.port
    
    @property
    def openstack_user_token(self):
        return self.openstack.token
