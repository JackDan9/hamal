# Copyright 2020 Hamal, Inc.

import functools
import six

from hamal.api import extensions
from hamal.api import server
from hamal.auth import login
from hamal.auth import register


def _create_controller(main_controller, action_controller_list):
    """This is a helper method to create controller with a 
    list of action controller
    """

    controller = server.wsgi.Resource(main_controller())
    for ctl in action_controller_list:
        controller.register_actions(ctl())
    return controller


login_controller = functools.partial(_create_controller,
                                     login.LoginController, [])
register_controller = functools.partial(_create_controller,
                                        register.RegisterController, [])


ROUTE_LIST = (
    ('/login', {
        'POST': [login_controller, 'login']
    }),
    ('/register', {
        'POST': [register_controller, 'register']
    })
)


class IdentityRouter(server.APIRouter):
    ExtensionManager = extensions.ExtensionManager

    def _setup_routes(self, mapper):
        for path, methods in ROUTE_LIST:
            if isinstance(methods, six.string_types):
                mapper.redirect(path, methods)
                continue

            for method, controller_info in methods.items():
                controller = controller_info[0]()
                action = controller_info[1]
                mapper.create_route(path, method, controller, action)
