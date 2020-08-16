# Copyright 2020 Hamal, Inc.

from oslo_config import cfg

CLI_ALL_OPTS = [
    cfg.ListOpt('mode',
                short='m',
                default=['create', 'export', 'update'],
                help='''
Create a new license or Export/Update an exit license
'''
),
    cfg.IntOpt('servers', 
               default=0,
               help='''
The numbers of server allowed by this new license, using in create mode.
'''
),
    cfg.IntOpt('days', 
               default=6, 
               help='''
The trial days allowed by this new license, using in create mode.
'''
),
    cfg.StrOpt('license', 
               default='', 
               help='''
An exist license, using in export mode.
''')
]


def register_opts(conf):
    conf.register_opts(CLI_ALL_OPTS)


def list_opts():
    return {'DEFAULT': CLI_ALL_OPTS}
