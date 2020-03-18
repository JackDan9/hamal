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

hamal_api_opts = [
    cfg.StrOpt(
        "hamal_api_listen",
        default="0.0.0.0",
        help="IP address on which hamal API listen."
    ),
    cfg.PortOpt(
        "hamal_api_listen_port",
        default=9278,
        help="Port on which hamal API listen."
    ),
    cfg.IntOpt(
        "hamal_api_workers",
        help="Number of workers for hamal API service. "
             "The default is equal to the number of CPUs available."
    ),
    cfg.BoolOpt(
        "use_rpc",
        default=False,
        help="Set True to enable RPC service."
    )
]


def register_opts(conf):
    conf.register_opts(hamal_api_opts)


def list_opts():
    return {'DEFAULT': hamal_api_opts}
