# Copyright

from oslo_log import log as logging

import hamal.conf
from hamal import rpc
from hamal import version
from hamal.db import api as db_api

CONF = hamal.conf.CONF


def prepare_logging(conf=None):
    """Prepare Oslo Logging

    Use of Oslo Logging involves the following
      * logging.register_options (required)
      * logging.set_defaults (optional)
      * logging.setup (required, setup will be done in main function)
    """
    if conf is None:
        conf = CONF

    logging.register_options(conf)

    extra_log_level_defaults = [
        'dogpile=INFO',
        'routes=INFO'
    ]
    logging.set_defaults(
        default_log_levels=logging.get_default_log_levels() +
        extra_log_level_defaults
    )


def parse_args(argv, domain='hamal', developer_config_files=None, configure_db=True, init_rpc=True):
    prepare_logging(CONF)

    CONF(argv[1:],
         project=domain,
         version=version.version_string(),
         default_config_files=developer_config_files)

    # Involve setup method to set up logging.
    # Usually we should set up logging after CONF(),
    # because the logging level and formatter
    # may be set in config files.
    logging.setup(CONF, domain)

    if init_rpc:
        rpc.init(CONF)

    if configure_db:
        db_api.register_models()
