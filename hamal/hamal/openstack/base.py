# Copyright 2020 Hamal, Inc.

from oslo_log import log as logging

from hamal.i18n import _, _LE


LOG = logging.getLogger(__name__)


class DataBase(object):
    """Base the data"""
    
    def __getattr__(self, name):
        try:
            return self.data[name]
        except KeyError:
            LOG.error(_LE("%(class_name)s object has no attribute %(name)s"), 
                                 {'class_name': self.__class__.__name__, 'name': name})
            raise AttributeError(_LE("%(class_name)s object has no attribute %(name)s"), 
                                 {'class_name': self.__class__.__name__, 'name': name})


class SourceBase(object):
    """Base the source"""

    def __init__(self, plugin, source_id):
        self.plugin = plugin
        self.id = source_id
    
    @classmethod
    def get_type(cls):
        return cls.__name__.lower()
    
    def get_id(self):
        return self.id
    
    def delete(self):
        pass
    
    def _check_failed_status(self, status):
        if status.upper() in ('ERROR', ):
            LOG.error(_LE("%(type)s %(id)s is ERROR", 
                          {'type': self.get_type, 'id': self.get_id}))
            raise Exception(_LE("%(type)s %(id)s is ERROR", 
                                {'type': self.get_type, 'id': self.get_id}))
