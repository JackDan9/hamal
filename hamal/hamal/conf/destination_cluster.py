# Copyright 2020 Hamal, Inc.


from oslo_config import cfg


destination_cluster_group = cfg.OptGroup(
    'destination_cluster',
    title='Destination Cluster Grouo',
    help='''
Options under this group are used to configure Destination Cluster.
Destination Cluster is used to handle destination cluster parameters.
'''
)

DESTINATION_CLUSTER_ALL_OPTS = [
    cfg.StrOpt(
        'ceph_conf_path',
        default='/etc/hamal/dest_ceph.conf',
        help='''
Destination cluster ceph configuration
'''
    ),
    cfg.StrOpt(
        'auth_url',
        default='http://192.168.2.82:5000',
        help='''
Destination cluster default authenticate url
'''
    ),
    cfg.StrOpt(
        'default_auth_name',
        default='admin',
        help='''
Destination cluster default authenticate username
'''
    ),
    cfg.StrOpt(
        'default_auth_password',
        default='admin',
        help='''
Destination cluster default authenticate password
'''
    ),
    cfg.StrOpt(
        'network_id',
        default='b3eb2a0d-26ea-43cb-9853-9b49eb51df01',
        help='''
Destination cluster network id
'''
    ),
    cfg.StrOpt(
        'floating_network_id',
        default='386200ea-6e57-460b-a6d0-27238eeafce2',
        help='''
Destination cluster floating network id
'''
    ),
    cfg.StrOpt(
        'glance_host',
        default='',
        help='''
Destination cluster glance host
'''
    )
]


def register_opts(conf):
    conf.register_group(destination_cluster_group)
    conf.register_opts(DESTINATION_CLUSTER_ALL_OPTS, group=destination_cluster_group)


def list_opts(conf):
    return {destination_cluster_group: DESTINATION_CLUSTER_ALL_OPTS}
