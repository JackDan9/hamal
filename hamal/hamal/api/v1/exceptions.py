# Copyright 2020 Hamal, Inc.


class BaseEx(Exception):
    pass


class vSpherePropertyNotExist(BaseEx):
    """The class for vsphere property not exist"""

    def __init__(self, object_type):
        self.message = ("Referenced type %s in property specification "
                        "does not exist. \n Consult the managed object "
                        "type reference in the vSphere API documentation."
                        % object_type)
    
    def __str__(self):
        return self.message
