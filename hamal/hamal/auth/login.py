# Copyright Hamal 2020, Inc.

import webob.exc
from webob import Response
from django.contrib.auth import authenticate # noqa

from hamal.api.server import wsgi
from hamal.db import api as db_api
from hamal.auth.token import create_token
from hamal.api.v1.token.check_token import check_user_token


class LoginController(wsgi.Controller):
    """The controller class for user login"""

    def __init__(self):
        super(LoginController, self).__init__()
    
    def login(self, req, body):
        username = body.get('username')
        password = body.get('password') 

        res = Response()
        
        verify_user = db_api.auth(username, password)
        if verify_user is None:
            raise webob.exc.HTTPUnauthorized
        
        user = {
            "email": verify_user.email,
            "id": verify_user.id,
            "extra": verify_user.extra,
            "default_project_id": verify_user.default_project_id
        }

        token = create_token(user=user)

        res.status = 200
        res.headerlist = [('Content-type', 'application/json')]
        res.json_body = {
            "access_token": str(token, encoding='utf-8'),
            "access_role": user.get('extra').get('user_role')
        }
        res.charset='UTF-8'
        
        return res

