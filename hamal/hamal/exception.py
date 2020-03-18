# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
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

"""Hamal base exception handling.

Includes decorator for re-raising Hamal-type exceptions.

SHOULD include dedicated exception logging.

"""

import sys

from oslo_config import cfg
from oslo_log import log as logging
import six
import webob.exc
from webob.util import status_generic_reasons
from webob.util import status_reasons

import hamal.conf
from hamal.i18n import _


LOG = logging.getLogger(__name__)

# exc_log_opts = [
#     cfg.BoolOpt('fatal_exception_format_errors',
#                 default=False,
#                 help='Make exception message format errors fatal.'),
# ]

# CONF = cfg.CONF
# CONF.register_opts(exc_log_opts)

CONF = hamal.conf.CONF


class ConvertedException(webob.exc.WSGIHTTPException):
    def __init__(self, code=500, title="", explanation=""):
        self.code = code
        # There is a strict rule about constructing status line for HTTP:
        # '...Status-Line, consisting of the protocol version followed by a
        # numeric status code and its associated textual phrase, with each
        # element separated by SP characters'
        # (http://www.faqs.org/rfcs/rfc2616.html)
        # 'code' and 'title' can not be empty because they correspond
        # to numeric status code and its associated text
        if title:
            self.title = title
        else:
            try:
                self.title = status_reasons[self.code]
            except KeyError:
                generic_code = self.code // 100
                self.title = status_generic_reasons[generic_code]
        self.explanation = explanation
        super(ConvertedException, self).__init__()


class Error(Exception):
    pass


class HamalException(Exception):
    """Base Hamal Exception

    To correctly use this class, inherit from it and define
    a 'message' property. That message will get printf'd
    with the keyword arguments provided to the constructor.

    """
    message = _("An unknown exception occurred.")
    code = 500
    headers = {}
    safe = False

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs
        self.kwargs['message'] = message

        if 'code' not in self.kwargs:
            try:
                self.kwargs['code'] = self.code
            except AttributeError:
                pass

        for k, v in self.kwargs.items():
            if isinstance(v, Exception):
                self.kwargs[k] = six.text_type(v)

        if self._should_format():
            try:
                message = self.message % kwargs

            except Exception:
                exc_info = sys.exc_info()
                # kwargs doesn't match a variable in the message
                # log the issue and the kwargs
                LOG.exception('Exception in string format operation')
                for name, value in kwargs.items():
                    LOG.error("%(name)s: %(value)s",
                              {'name': name, 'value': value})
                if CONF.fatal_exception_format_errors:
                    six.reraise(*exc_info)
                # at least get the core message out if something happened
                message = self.message
        elif isinstance(message, Exception):
            message = six.text_type(message)

        # NOTE(luisg): We put the actual message in 'msg' so that we can access
        # it, because if we try to access the message via 'message' it will be
        # overshadowed by the class' message attribute
        self.msg = message
        super(HamalException, self).__init__(message)

    def _should_format(self):
        return self.kwargs['message'] is None or '%(message)' in self.message

    # NOTE(tommylikehu): This method can be used to
    # translate translatable variables (Message object here), do not
    # wrap it with str(), unicode(), six.text_type().
    def __unicode__(self):
        return self.msg


class Invalid(HamalException):
    message = _("Unacceptable parameters.")
    code = 400


class InvalidContentType(Invalid):
    message = _("Invalid content type %(content_type)s.")


class InvalidInput(Invalid):
    message = _("Invalid input received: %(reason)s")


class MalformedRequestBody(HamalException):
    message = _("Malformed message body: %(reason)s")


class NotAuthorized(HamalException):
    message = _("Not authorized.")
    code = 403


class NotFound(HamalException):
    message = _("Resource could not be found.")
    code = 404
    safe = True


class ConfigNotFound(NotFound):
    message = _("Could not find config at %(path)s")


class PasteAppNotFound(NotFound):
    message = _("Could not load paste app '%(name)s' from %(path)s")


class ServiceNotFound(NotFound):

    def __init__(self, message=None, **kwargs):
        if not message:
            if kwargs.get('host', None):
                self.message = _("Service %(service_id)s could not be "
                                 "found on host %(host)s.")
            else:
                self.message = _("Service %(service_id)s could not be found.")
        super(ServiceNotFound, self).__init__(message, **kwargs)


class LicenseExc(ConvertedException):
    def __init__(self, code=593, title="", explanation=""):
        self.code = code
        if title:
            self.title = title
        else:
            try:
                self.title = status_reasons[self.code]
            except KeyError:
                generic_code = self.code // 100
                self.title = status_generic_reasons[generic_code]
        self.explanation = explanation
        super(ConvertedException, self).__init__()
