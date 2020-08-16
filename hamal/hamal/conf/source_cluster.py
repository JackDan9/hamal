# Copyright 2020 Hamal, Inc.

from oslo_config import cfg


source_cluster_group = cfg.OptGroup(
    'source_cluster',
    title='Source Cluster Group',
    help='''
Options under this group are used to configure Source Cluster.
Source Cluster is used to handle source cluster parameters.
'''
)


SOURCE_CLUSTER_ALL_OPTS = [
    cfg.StrOpt(
        'ceph_conf_path',
        default='/etc/hamal/source_ceph.conf',
        help='''
Source Cluster ceph configuration path
'''
    ),
    cfg.StrOpt(
        'auth_url',
        default='http://192.168.1.2:5000',
        help='''
Source Cluster authenticate url
'''
    ),
    cfg.StrOpt(
        'default_auth_name',
        default='admin',
        help='''
Source Cluster authenticate name
'''
    ),
    cfg.StrOpt(
        'default_auth_password',
        default='passw0rd',
        help='''
Source Cluster authenticate password
'''
    )
]


def register_opts(conf):
    conf.register_group(source_cluster_group)
    conf.register_opts(SOURCE_CLUSTER_ALL_OPTS, group=source_cluster_group)

def list_opts():
    return {source_cluster_group: SOURCE_CLUSTER_ALL_OPTS}
