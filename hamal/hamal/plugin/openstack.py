# Copyright 2020 Hamal, Inc.

import time
import calendar
import urllib.parse
from datetime import datetime

from oslo_log import log as logging

from hamal.plugin import nova
from hamal.plugin import cinder
from hamal.plugin import neutron
from hamal.plugin import glance
from hamal.exception import HttpException, HamalException
from hamal.utils.plugin import post_request, is_req_success
from hamal.plugin.utils import transfer_datetime
from hamal.i18n import _, _LE, _LW, _LI
import hamal.conf


LOG = logging.getLogger(__name__)
CONF = hamal.conf.CONF

CLUSTER_PLUGIN = {}


CLUSTERS = {
    'source': {
        'ceph_conf_path': CONF.source_cluster.ceph_conf_path,
        'auth_url': CONF.source_cluster.auth_url,
        'default_auth_name': CONF.source_cluster.default_auth_name,
        'default_auth_password': CONF.source_cluster.default_auth_password
    },
    'destination': {
        'ceph_conf_path': CONF.destination_cluster.ceph_conf_path,
        'auth_url': CONF.destination_cluster.auth_url,
        'default_auth_name': CONF.destination_cluster.default_auth_name,
        'default_auth_password': CONF.destination_cluster.default_auth_password,
        'network_id': CONF.destination_cluster.network_id,
        'floating_network_id': CONF.destination_cluster.floating_network_id,
        'glance_host': CONF.destination_cluster.glance_host or None
    }
}


class OpenstackPlugin(object):
    """A plugin of Openstack"""

    def __init__(self, auth_url, cluster_name, username, password, tenant_id):
        self.cluster_name = cluster_name
        # self.auth_url = CLUSTERS.get(cluster_name)['auth_url']
        self.auth_url = auth_url
        self.username = username
        self.password = password
        self.tenant_id = tenant_id

        self._openstack_user_token = None
        self._openstack_user_token_expire = None
        self.service_catalog = None

        self.nova = None
        self.cinder = None
        self.neutron = None
        self.glance = None

        self.auth()
        self.init_services()

        self.ceph_conf_path = str(CLUSTERS.get(cluster_name)['ceph_conf_path'])

    @property
    def openstack_user_token(self):
        if time.time() > self._openstack_user_token_expire:
            self.auth()
        return self._openstack_user_token
    
    def auth(self):
        auth_url = self.auth_url + '/v2.0/tokens'
        data = {
            "auth": {
                "passwordCredentials": {
                    "username": self.username,
                    "password": self.password
                }
            }
        }

        try:
            resp_data = post_request(url=auth_url, body=data)
        except Exception as e:
            LOG.exception(_LW("Hamal openstack authentication PasswordCredentials exception ERROR_CLUSTER : [%(cluster_name)s], ERROR_CONTENT : %(message)s"), 
                              {"cluster_name": self.cluster_name, "message": e})
            raise HttpException(code=401, message="Cluster [%s] auth error : %s" % (self.cluster_name, str(e)))

        openstack_user_token = resp_data['access']['token']['id']
        data = {
            "auth": {
                "tenantId": self.tenant_id,
                "token": {
                    "id": openstack_user_token
                }
            }
        }

        try:
            resp_data = post_request(url=auth_url, body=data)
        except Exception as e:
            LOG.exception(_LW("Hamal openstack authentication TenantId exception ERROR_CLUSTER : [%(cluster_name)s], ERROR_CONTENT : %(message)s"), 
                          {"cluster_name": self.cluster_name, "message": str(e)})
            raise HttpException(code=401, message="Cluster [%s] auth error : %s" % (self.cluster_name, str(e)))
        
        self._openstack_user_token = resp_data['access']['token']['id']

        token_expire_timestamp = calendar.timegm(datetime.strptime(transfer_datetime(resp_data['access']['token']['expires']),  "%Y-%m-%d %H:%M:%S").timetuple())
        LOG.info(_LI("Hamal openstack user token expire timestamp is %(timestamp)s"), {"timestamp": token_expire_timestamp})
        
        self._openstack_user_token_expire = token_expire_timestamp - 300
        self.service_catalog = resp_data
    
    def get_service_url(self, service_name):
        for service in self.service_catalog['access']['serviceCatalog']:
            if service_name == service['name']:
                return service['endpoints'][0]['publicURL']
        
        LOG.exception(_LE("Hamal endpoint exception service name : %(service_name)s"), 
                          {"service_name": service_name})
        raise HttpException(code=400, message="%s endpoint not found" % service_name)

    def init_services(self):
        nova_url = self.get_service_url('nova')
        cinder_url = self.get_service_url('cinder')
        neutron_url = self.get_service_url('neutron')
        glance_host = CLUSTERS.get(self.cluster_name).get('glance_host')
        if glance_host is not None:
            glance_url = glance_host
        else:
            glance_url = self.get_service_url('Image Service')
        
        self.nova = nova.NovaPlugin(nova_url, self)
        self.cinder = cinder.CinderPlugin(cinder_url, self)
        self.neutron = neutron.NeutronPlugin(neutron_url, self)
        self.glance = glance.GlancePlugin(glance_url, self)
