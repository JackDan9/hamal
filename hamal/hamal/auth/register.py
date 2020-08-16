# Copyright 2020 Hamal, Inc.

import uuid

import six

from hamal.api.server import wsgi
from hamal.db import api as db_api

class RegisterController(wsgi.Controller):
    """The class for register"""

    def __init__(self):
        super(RegisterController, self).__init__()
    
    def register(self, req, body):
        pass
