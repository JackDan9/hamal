# Copyright 2020 Hamal, Inc.

from oslo_log import log as logging
import webob.exc

from hamal.wsgi import common as base_wsgi
from hamal.auth.token import verify_token


LOG = logging.getLogger(__name__)


class AuthWrapper(base_wsgi.Middleware):
    """Just a simple auth wrapper

    if we check a user property with token, we consider it auth.
    """

    @webob.dec.wsgify(RequestClass=base_wsgi.Request)
    def __call__(self, req):
        headers = req.headers

        token = verify_token(token=headers.get('account_token'))
        if headers.get('account_token') is None or not token:
            raise webob.exc.HTTPUnauthorized
        return self.application
        