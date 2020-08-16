# Copyright 2012 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""SQL backends for the various services.

Before using this module, call initialize(). This has to be done before 
CONF() because it sets up configuration options.

"""

from oslo_serialization import jsonutils
from sqlalchemy import Text 
from sqlalchemy import types as sql_types


# Special Text Field
class JsonBlob(sql_types.TypeDecorator):

    impl = Text

    def process_bind_param(self, value, dialect):
        return jsonutils.dumps(value)
    
    def process_result_value(self, value, dialect):
        if value is not None:
            value = jsonutils.loads(value)
        return value
