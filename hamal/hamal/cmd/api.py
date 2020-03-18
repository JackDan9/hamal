# Copyright

import os
import sys

import eventlet
from oslo_log import log as logging
from oslo_reports import opts as gmr_opts

import hamal.conf
from hamal import config
from hamal import service

eventlet.monkey_patch()

CONF = hamal.conf.CONF
LOG = logging.getLogger(__name__)

possible_topdir = os.path.normpath(os.path.join(os.path.abspath(__file__),
                                                os.pardir,
                                                os.pardir,
                                                os.pardir))
if os.path.exists(os.path.join(possible_topdir,
                               'hamal',
                               '__init__.py')):
    sys.path.insert(0, possible_topdir)


def main():
    gmr_opts.set_defaults(CONF)

    developer_config = os.path.join(possible_topdir, 'etc', 'hamal.conf')

    if not os.path.exists(developer_config):
        developer_config = None

    if developer_config:
        developer_config = [developer_config]

    config.parse_args(sys.argv,
                      domain='hamal',
                      developer_config_files=developer_config)

    server = service.WSGIService('hamal_api')
    launcher = service.process_launcher()
    launcher.launch_service(server, workers=server.workers or 1)
    launcher.wait()
