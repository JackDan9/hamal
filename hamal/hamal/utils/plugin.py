# Copyright 2020 Hamal, Inc.

import uuid
import json
import threading
import urllib
from urllib.error import HTTPError

from oslo_log import log as logging

from hamal.i18n import _, _LE, _LI, _LW
from hamal.exception import HamalException
from webob import Request
import requests
from requests import HTTPError


LOG = logging.getLogger(__name__)


request_state = threading.local()


def is_req_success(code):
    if code in (200, 201, 202, 204):
        return True
    return False


def post_request(url, body, token=None, no_resp_content=False):
    request_id = get_request_id()

    # if isinstance(body, dict):
    #    body = json.dumps(body)
    
    headers = {"Content-type": "application/json"}

    if token is not None:
        headers['X-Auth-Token'] = token

    post_info = "[%s] : curl -X POST '%s' -d '%s' %s" % (
        request_id, url, body, ' '.join([' -H "%s:%s"' % (key, value) for key, value in headers.items()])
    )

    try:
        LOG.info(_LI("Hamal post request information: %(post_info)s"), 
                     {'post_info': post_info})
        response = requests.post(url=url, json=body, headers=headers)
        # req = urllib.request.Request(url, data=bytes(urllib.parse.urlencode(body), 'utf8'), headers=headers)
        # response = urllib.request.urlopen(req)
    except HTTPError as he:
        error_msg = he.fp.read()

        LOG.error(_LE("Hamal post request http error information '[%(request_id)s]' %(post_info)s EXCEPTION : %(error_msg)s"), 
                      {"request_id": request_id, "post_info": post_info, "error_msg": error_msg})
        raise HamalException(message=error_msg)
    except Exception as e:
        LOG.exception(_LE("Hamal post request http exception information '[%(request_id)s]' %(post_info)s EXCEPTION : '%(e)s"), 
                          {"request_id": request_id, "post_info": post_info, "e": e})
        raise e
    
    code = response.status_code
    content = response.content.decode()

    if is_req_success(code):
        LOG.info(_LI("Hamal post request http success information '[%(request_id)s]' : RESP CODE : '%(code)s', RESP DATA : '%(content)s'"), 
                     {"request_id": request_id, "code": code, "content": content})
        if no_resp_content:
            return
        return json.loads(content)

    LOG.error(_LE("Hamal post request http success information '[%(request_id)s]' : RESP CODE : '%(code)s', RESP DATA '%(content)s'"), 
                  {"request_id": request_id, "code": code, "content": content})
    raise HamalException(message=content)


def update_request(url, body, token=None, no_resp_content=False):
    request_id = get_request_id()

    # if isinstance(body, dict):
        # body = json.dumps(body)
    
    headers = {"Content-type": "application/json"}
    if token is not None:
        headers['X-Auth-Token'] = token
    
    post_info = "[%s] : curl -X PUT '%s' -d '%s' %s" % (
        request_id, url, body, ' '.join([' -H "%s: %s"' % (key, value) for key, value in headers.items()])
    )

    try:
        LOG.info(_LI("Hamal update request information : %(post_info)s", 
                     {"post_info": post_info}))
        response = requests.put(url=url, json=body, headers=headers)
        # req = urllib.request.Request(url, body, headers=headers)
        # req.get_method = lambda: 'PUT'
        # response = urllib.request.urlopen(req)
    except HTTPError as he:
        error_msg = he.fp.read()
        LOG.error(_LE("Hamal update request error information '[%(request_id)s]' %(post_info)s ERROR : %(error_msg)s"), 
                      {"request_id": request_id, "post_info": post_info, "error_msg": error_msg})
        raise HamalException(message=error_msg)
    except Exception as e:
        LOG.exception(_LE("Hamal update request exception information: '[%(request_id)s]' %(post_info)s EXCEPTION : %(e)s"), 
                          {"request_id": request_id, "post_info": post_info, "e": e})
        raise e
    
    code = response.status_code
    content = response.content

    if is_req_success(code):
        LOG.info(_LI("Hamal update request success information '[%(request_id)s]' : RESP_CODE : %(code)s, RESP DATA : %(content)s"), 
                     {"request_id": request_id, "code": code, "content": content})
        if no_resp_content:
            return
        return json.loads(content)
    
    LOG.error(_LE("Hamal update request error information '[%(request_id)s' : RESP_CODE : %(code)s, RESP_DATA : %(content)s"), 
                  {"request_id": request_id, "code": code, "content": content})
    raise HamalException(message=content)


def get_request(url, token, body=None):
    request_id = get_request_id()

    headers = {"Accept": "application/json",
               "X-Auth-Token": token}
    
    get_info = "[%s] : curl -X GET '%s' %s" % (
        request_id, url, ' '.join([' -H "%s : %s"' % (key, value) for key, value in headers.items()])
    )

    try:
        LOG.info(_LI("Hamal get request information : %(get_info)s"), 
                     {"get_info": get_info})
        response = requests.get(url=url, headers=headers)

        # req = urllib.request.Request(url, headers=headers)
        # response = urllib.request.urlopen(req)
    except HTTPError as he:
        error_msg = he.fp.read()
        LOG.error(_LE("Hamal get request error information : [%(request_id)s] %(get_info)s ERROR : %(error_msg)s"), 
                      {"request_id": request_id, "get_info": get_info, "error_msg": error_msg})
        raise HamalException(message=error_msg)
    except Exception as e:
        LOG.error(_LE("Hamal get request exception information : [%(request_id)s] %(get_info)s EXCEPTION : %(e)s"), 
                      {"request_id": request_id, "get_info": get_info, "e": e})
        raise e
    
    code = response.status_code
    content = response.content

    if is_req_success(code):
        LOG.info(_LI("Hamal get request success information [%(request_id)s] : RESP CODE : %(get_info)s, RESP DATA : %(content)s"), 
                     {"request_id": request_id, "get_info": get_info, "content": content})
        # change to dict eval(content)
        return json.loads(content)
    
    LOG.error(_LE("Hamal get request error information [%(request_id)s] : RESP CODE : %(get_info)s, RESP DATA : %(content)s"), 
                  {"request_id": request_id, "get_info": get_info, "content": content})
    raise HamalException(message=content)


def delete_request(url, token, body=None):
    request_id = get_request_id()

    headers = {"Accept": "application/json",
               "X-Auth-Token": token}
    
    get_info = "[%s] : curl -X DELETE '%s' %s" % (
        request_id, url, ' '.join([' -H "%s : %s"' % (key, value) for key, value in headers.items()])
    )

    try:
        LOG.info(_LI("Hamal delete request information : %(get_info)s"), 
                     {"get_info": get_info})
        response = requests.delete(url=url, headers=headers)
        # req = urllib.request.Request(url, headers=headers)
        # req.get_method = lambda: 'DELETE'
        # response = urllib.request.urlopen(req)
    except HTTPError as he:
        error_msg = he.fp.read()

        if he.code == 404 and error_msg == '{"itemNotFound": {"message": "The resource could not be found.", "code": 404}}':
            return True
        
        LOG.error(_LE("Hamal delete request error information : [%(request_id)s] %(get_info)s ERROR : %(error_msg)s"), 
                      {"request_id": request_id, "get_info": get_info, "error_msg": error_msg})
        raise HamalException(message=error_msg)
    except Exception as e:
        LOG.error(_LE("Hamal delete request [%(request_id)s] %(get_info)s, EXCEPTION : %(e)s"), 
                      {"request_id": request_id, "get_info": get_info, "e": e})
        raise e
    
    code = response.status_code
    content = response.content

    if is_req_success(code):
        LOG.info(_LI("Hamal delete request success information : [%(request_id)s] : RESP CODE : %(code)s, RESP DATA : %(content)s"), 
                     {"request_id": request_id, "code": code, "content": content})
        return True
    
    LOG.error(_LE("Hamal delete request error information : [%(request_id)s] : RESP CODE : %(code)s, RESP DATA : %(content)s"), 
                  {"request_id": request_id, "code": code, "content": content})
    raise HamalException(message=content)


def set_request_id(request_id):
    request_state.request_id = request_id


def get_request_id():
    return hasattr(request_state, 'request_id') and request_state.request_id or None
