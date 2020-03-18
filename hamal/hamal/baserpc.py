# Copyright 2013 Red Hat, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#

"""
Base RPC client and server common to all services.
"""

import oslo_messaging as messaging
from oslo_serialization import jsonutils

import hamal.conf
from hamal import rpc


CONF = hamal.conf.CONF

_NAMESPACE = 'baseapi'


class BaseAPI(object):
    """Client side of the base rpc API.

    API version history:

        1.0 - Initial version.
    """

    VERSION_ALIASES = {
    }

    def __init__(self, topic):
        super(BaseAPI, self).__init__()
        target = messaging.Target(topic=topic,
                                  namespace=_NAMESPACE,
                                  version='1.0')
        self.client = rpc.get_client(target)

    def ping(self, context, arg, timeout=None):
        arg_p = jsonutils.to_primitive(arg)
        cctxt = self.client.prepare(timeout=timeout)
        return cctxt.call(context, 'ping', arg=arg_p)


class BaseRPCAPI(object):
    """Server side of the base RPC API."""

    target = messaging.Target(namespace=_NAMESPACE, version='1.0')

    def __init__(self, service_name):
        self.service_name = service_name

    def ping(self, context, arg):
        resp = {'service': self.service_name, 'arg': arg}
        return jsonutils.to_primitive(resp)
