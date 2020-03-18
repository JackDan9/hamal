# Copyright

import copy
import itertools

from hamal.api import extensions
from hamal.api.middleware import auth
from hamal.engine import manager
from hamal import service
from hamal.wsgi import server


def list_opts():
    """Entry point for oslo-config-generator."""
    return [('DEFAULT', itertools.chain(
        copy.deepcopy(auth.auth_opts),
        copy.deepcopy(extensions.extension_opts),
        copy.deepcopy(manager.engine_opts),
        copy.deepcopy(server.wsgi_opts),
        copy.deepcopy(service.service_opts)))]
