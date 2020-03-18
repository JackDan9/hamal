# Copyright 

import webob.exc

from hamal.api import extensions
from hamal.api.server import wsgi
from hamal.i18n import _


class DemoTagController(wsgi.Controller):

    @staticmethod
    def _extract_tag(body):
        tag = None
        attr = "%s:tag" % Demo_tag.alias
        try:
            if attr in body:
                tag = body[attr]
        except ValueError:
            msg = _("malformed demo attribute")
            raise webob.exc.HTTPBadRequest(explanation=msg)

        return tag

    @wsgi.extends
    def create(self, req, body):
        tag = self._extract_tag(body)
        if tag:
            body["state"] = str(tag) + ":" + body["state"]
        yield


class Demo_tag(extensions.ExtensionDescriptor):
    """pass arbitrary key/value pairs to the demo"""
    name = "DemoTag"
    alias = "DEMO_TAG"
    updated = "2017-11-07T19:25:27-05:00"

    def get_controller_extensions(self):
        controller = DemoTagController()
        extension = extensions.ControllerExtension(self, 'demos', controller)
        return [extension]
