# Copyright 2015 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_config import cfg
from oslo_db import options as oslo_db_options


_DEFAULT_SQL_CONNECTION = 'mysql+pymysql://root:passw0rd@127.0.0.1/hamal'
_ENRICHED = False


# NOTE(jackdan): We cannot simply do:
# conf.register_opts(oslo_db_options.database_opts, 'api_database')
# If we reuse a db config option for two different groups ("api_database"
# and "database") and deprecate or rename a config option in one of these
# groups, "oslo.config" cannot correctly determine which one to update.
# That's why we copied & pasted these config options for the "api_database"
# group here.
api_db_group = cfg.OptGroup('api_database',
    title='API Database Options',
    help="""
The *Hamal API Database* is a separate database which is used for information
which is used across *cells*.
""")

api_db_opts = [
    # TODO(jackdan): This should probably have a required=True attribute
    cfg.StrOpt('connection',
        secret=True,
        # This help gets appended to the oslo.db help so prefix with a space.
        help=''),
    cfg.StrOpt('connection_parameters',
        default='',
        help=''),
    cfg.BoolOpt('sqlite_synchronous',
        default=True,
        help=''),
    cfg.StrOpt('slave_connection',
        secret=True,
        help=''),
    cfg.StrOpt('mysql_sql_mode',
        default='TRADITIONAL',
        help=''),
    cfg.IntOpt('connection_recycle_time',
        default=3600,
        deprecated_name='idle_timeout',
        help=''),
    # TODO(jackdan): We should probably default this to 5 to not rely on the
    # SQLAlchemy default. Otherwise we wouldn't provide a stable default.
    cfg.IntOpt('max_pool_size',
        help=''),
    cfg.IntOpt('max_retries',
        default=10,
        help=''),
    # TODO(jackdan): This should have a minimum attribute of 0
    cfg.IntOpt('retry_interval',
        default=10,
        help=''),
    # TODO(jackdan): We should probably default this to 10 to not rely on the
    # SQLAlchemy default. Otherwise we wouldn't provide a stable default.
    cfg.IntOpt('max_overflow',
        help=''),
    # TODO(jackdan): This should probably make use of the "choices" attribute.
    # "oslo.db" uses only the values [<0, 0, 50, 100] see module
    # /oslo_db/sqlalchemy/engines.py method "_setup_logging"
    cfg.IntOpt('connection_debug',
        default=0,
        help=''),
    cfg.BoolOpt('connection_trace',
        default=False,
        help=''),
    # TODO(jackdan): We should probably default this to 30 to not rely on the
    # SQLAlchemy default. Otherwise we wouldn't provide a stable default.
    cfg.IntOpt('pool_timeout',
        help='')
]  # noqa


def enrich_help_text(alt_db_opts):

    def get_db_opts():
        for group_name, db_opts in oslo_db_options.list_opts():
            if group_name == 'database':
                return db_opts
        return []

    for db_opt in get_db_opts():
        for alt_db_opt in alt_db_opts:
            if alt_db_opt.name == db_opt.name:
                # NOTE(jackdan): We can append alternative DB specific help
                # texts here if needed.
                alt_db_opt.help = db_opt.help + alt_db_opt.help


def register_opts(conf):
    oslo_db_options.set_defaults(conf, connection=_DEFAULT_SQL_CONNECTION)
    conf.register_opts(api_db_opts, group=api_db_group)


def list_opts():
    # NOTE(jackdan): 2016-04-04: If we list the oslo_db_options here, they
    # get emitted twice(!) in the "sample.conf" file. First under the
    # namespace "hamal.conf" and second under the namespace "oslo.db". This
    # is due to the setting in file "etc/hamal/hamal-config-generator.conf".
    # As I think it is useful to have the "oslo.db" namespace information
    # in the "sample.conf" file, I omit the listing of the "oslo_db_options"
    # here.
    global _ENRICHED
    if not _ENRICHED:
        enrich_help_text(api_db_opts)
        _ENRICHED = True
    return {
        api_db_group: api_db_opts,
    }
