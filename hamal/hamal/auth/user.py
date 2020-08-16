# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import hashlib

from oslo_log import log as logging
import six

from hamal.i18n import _, _LE, _LC, _LI, _LW

LOG = logging.getLogger(__name__)
# parameter need to write configure
_TOKEN_HASH_ENABLED = True


def set_session_from_user(request, user):
    request.session['token'] = user.token
    request.session['user_id'] = user.id
    # Update the user object cached in the request
    request._cached_user = user
    request.user = user


def create_user_from_token(request, token):
    # if the 
    pass


class User(object):
    """A User class with some extra special sauce for 
    """
    pass
