# Copyright 2020 Hamal, Inc.

from oslo_log import log as logging

from hamal.exception import HamalException
from hamal.openstack.base import DataBase
from hamal.openstack.base import SourceBase
from hamal.i18n import _, _LW, _LE


LOG = logging.getLogger(__name__)


class FlavorData(DataBase):
    """A class of flavor data"""

    def __init__(self, data):
        self.data = data['flavor']
    
    @property
    def vcpus(self):
        pass
