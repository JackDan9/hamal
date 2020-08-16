# Copyright 2020 Hamal, Inc.

from hamal.api.server import wsgi
from hamal.api.views.openstack import instances as instances_view


class InstancesController(wsgi.Controller):
    """The class for Instances on openstack"""

    _view_builder_class = instances_view.ViewBuilder

    def __init__(self):
        super(InstancesController, self).__init__()
    
    def index(self, req):
        return self._get_allow_instance_numbers(req)
    
    def create(self, req, body):
        return self._get_instances_on_openstack(req, body)
    
    # backend resources operation
    def _get_allow_instance_numbers(self, req):
        return self._view_builder._allow_instance_numbers(req)
    
    def _get_instances_on_openstack(self, req, body):
        return self._view_builder._instance_list(req, body)
