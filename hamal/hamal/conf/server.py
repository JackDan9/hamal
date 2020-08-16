# Copyright 2020 Hamal, Inc.

from oslo_config import cfg


server_group = cfg.OptGroup(name='server',
                            title='Hamal Host Name')

SERVER_ALL_OPTS = [
    cfg.StrOpt('server_name',
               default='hamal-host')
]


def register_opts(conf):
    conf.register_group(server_group)
    conf.register_opts(SERVER_ALL_OPTS, group=server_group)


def list_opts():
    return {server_group: SERVER_ALL_OPTS}
