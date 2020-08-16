# _*_ coding:utf-8 _*_
from datetime import datetime, timedelta

import jwt
from oslo_log import log as logging

import hamal.conf
from hamal import exception
from hamal.i18n import _, _LE, _LI


CONF = hamal.conf.CONF
LOG = logging.getLogger(__name__)


def create_token(user):
    """Create token by user information

    :param user: context to user information
    """

    payload = {
        'username': user['email'],
        'id': user['id'],
        'extra': user['extra'],
        'default_project_id': user['default_project_id'],
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=1)
    }

    token = jwt.encode(payload, CONF.token.secret, algorithm='HS256')
    return token


def verify_token(token):
    """Verify token information
    
    :param token: context to token information
    """

    try:
        payload = jwt.decode(token, CONF.token.secret, algorithms=['HS256'])
        payload['email'] = payload['username']
        token = create_token(payload)
        return token
    except:
        LOG.exception(_LE('Verify token exception!'))
        return False
