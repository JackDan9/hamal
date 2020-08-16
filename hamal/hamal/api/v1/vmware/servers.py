# Copyright 2020 Hamal, Inc.

from hamal.api.server import wsgi
from hamal.api.views.vmware import servers as servers_view


class ServersController(wsgi.Controller):
    """The class for VirtualMachines on vmware vsphere vcenter"""

    _view_builder_class = servers_view.ViewBuilder

    def __init__(self):
        super(ServersController, self).__init__()
    
    def index(self, req):
        return self._get_allow_server_numbers(req)
    
    def create(self, req, body):
        return self._get_servers_on_esxi(req, body)

    # backend resources operation
    def _get_allow_server_numbers(self, req):
        return self._view_builder._allow_server_numbers(req)
    
    def _get_servers_on_esxi(self, req, body):
        return self._view_builder._server_list(req, body)
