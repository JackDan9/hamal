# Copyright 2020 Hamal, Inc.

from hamal.utils.plugin import get_request, post_request, delete_request, update_request


NETWORKS_URL = '/v2.0/network.json'
NETWORK_URL = '/v2.0/networks/{network_id}.json'

FLOATING_IPS_URL = '/v2.0/floatingips.json'
FLOATING_IP_URL = '/v2.0/floatingips/{floatingip}.json'

PORTS_URL = '/v2.0/ports.json'
PORT_URL = '/v2.0/ports/{port_id}.json'

SECURITY_GROUPS_URL = '/v2.0/security-groups.json'
SECURITY_GROUP_URL = '/v2.0/security-groups/{security_group_id}.json'

SECURITY_GROUP_RULES_URL = '/v2.0/security-group-rules.json'
SECURITY_GROUP_RULE_URL = '/v2.0/security-group-rules/{security_group_rule_id}.json'


class NeutronPlugin(object):
    """A plugin of Neutron"""

    def __init__(self, host_url, openstack):
        self.host_url = host_url
        self.openstack = openstack
        self._networks_url = self.host_url + NETWORKS_URL
        self._network_url = self.host_url + NETWORK_URL
        self._floating_ips_url = self.host_url + FLOATING_IPS_URL
        self._floating_ip_url = self.host_url + FLOATING_IP_URL
        self._ports_url = self.host_url + PORTS_URL
        self._port_url = self.host_url + PORT_URL
        self._security_groups_url = self.host_url + SECURITY_GROUPS_URL
        self._security_group_url = self.host_url + SECURITY_GROUP_URL
        self._security_group_rules_url = self.host_url + SECURITY_GROUP_RULES_URL
        self._security_group_rule_url = self.host_url + SECURITY_GROUP_RULE_URL

    @property
    def openstack_user_token(self):
        return self.openstack.token
    
    def get_network(self, network_id):
        network_url = self._network_url.format(network_id=network_id)
        return get_request(network_url, self.openstack_user_token)
    
    def get_networks(self):
        return get_request(self._networks_url, self.openstack_user_token)
    
    def create_floatingip(self, net_id, ip, port_id):
        data = {
            "floatingip": {
                "floating_network_id": net_id,
                "floating_ip_address": ip,
                "port_id": port_id
            }
        }

        return post_request(self._floating_ips_url, data, self.openstack_user_token)
    
    def delete_floatingip(self, floatingip_id):
        floatingip_url = self._floating_ip_url.format(floatingip_id=floatingip_id)
        return delete_request(floatingip_url, self.openstack_user_token)

    def get_port(self, port_id):
        port_url = self._port_url.format(port_id=port_id)
        return get_request(port_url, self.openstack_user_token)

    def update_port(self, port_id, security_groups):
        port_url = self._port_url.format(port_id=port_id)
        data = {
            "port": {
                "security_groups": security_groups
            }
        }

        return update_request(port_url, data, self.openstack_user_token)

    def get_security_group(self, security_group_id):
        security_group_url = self._security_group_url.format(security_group_id=security_group_id)
        return get_request(security_group_url, self.openstack_user_token)
    
    def delete_security_group(self, security_group_id):
        security_group_url = self._security_group_url.format(security_group_id=security_group_id)
        return delete_request(security_group_url, self.openstack_user_token)

    def create_security_group(self, name):
        if name == 'default':
            name = 'hamal-default'
        data = {
            "security_group": {
                "name": name
            }
        }

        return post_request(self._security_groups_url, data, self.openstack_user_token)
    
    def delete_security_group_rule(self, security_group_rule_id):
        security_group_rule_url = self._security_group_rule_url.format(security_group_rule_id=security_group_rule_id)
        return delete_request(security_group_rule_url, self.openstack_user_token)
    
    def create_security_group_rule(self, security_group_id, direction, ethertype, port_range_max,
                                   port_range_min, protocol, remote_group_id, remote_ip_prefix):
        data = {
            "security_group_rule": {
                "security_group_id": security_group_id,
                "direction": direction,
                "ethertype": ethertype,
                "port_range_max": port_range_max,
                "port_range_min": port_range_min,
                "protocol": protocol,
                "remote_group_id": remote_group_id,
                "remote_ip_prefix": remote_ip_prefix
            }
        }

        return post_request(self._security_group_rules_url, data, self.openstack_user_token)
