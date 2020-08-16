# Copyright
#
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

from oslo_config import cfg

token_group = cfg.OptGroup(
    'token',
    title='TOKEN Group',
    help='''
Options under this group are used to configure TOKEN. TOKEN is used to serve API requests. 
'''
)

TOKEN_ALL_OPTS = [
    cfg.StrOpt(
        "secret",
        default="hamal secret",
        help="The default value of hamal token secret."
    )
]


def register_opts(conf):
    conf.register_group(token_group)
    conf.register_opts(TOKEN_ALL_OPTS, group=token_group)


def list_opts():
    return { token_group: TOKEN_ALL_OPTS }