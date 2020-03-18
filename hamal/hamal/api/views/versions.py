# Copyright

import copy
import re


def get_view_builder(req):
    base_url = req.application_url
    return ViewBuilder(base_url)


class ViewBuilder(object):
    def __init__(self, base_url):
        """Initialize ViewBuilder.

        :param base_url: url of the root wsgi application
        """
        self.base_url = base_url

    def build_versions(self, versions):
        views = [self._build_version(versions[key])
                 for key in sorted(list(versions.keys()))]
        return dict(versions=views)

    def _build_version(self, version):
        view = copy.deepcopy(version)
        return view

    def _get_base_url_without_version(self):
        """Get the base URL with out the /v1 suffix."""
        return re.sub('v[1-9]+/?$', '', self.base_url)
