# Copyright

import functools
import six

from hamal.api import extensions
from hamal.api import server
from hamal.api import versions
from hamal.api.v1.vmware import servers
from hamal.api.v1.openstack import instances


def _create_controller(main_controller, action_controller_list):
    """This is a helper method to create controller with a
    list of action controller.
    """
    controller = server.wsgi.Resource(main_controller())
    for ctl in action_controller_list:
        controller.register_actions(ctl())
    return controller


version_controller = functools.partial(_create_controller,
                                       versions.VersionsController, [])
server_controller = functools.partial(_create_controller,
                                      servers.ServersController, [])
instance_controller = functools.partial(_create_controller,
                                        instances.InstancesController, [])


ROUTE_LIST = (
    ('', '/'),
    ('/', {
        'GET': [version_controller, 'index']
    }),
    ('/servers', {
        'GET': [server_controller, 'index'],
        'POST': [server_controller, 'create']
    }),
    ('/instances', {
        'GET': [instance_controller, 'index'],
        'POST': [instance_controller, 'create']
    })
)


class APIRouter(server.APIRouter):
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