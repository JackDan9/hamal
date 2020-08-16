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

wsgi_group = cfg.OptGroup(
    'wsgi',
    title='WSGI Group',
    help='''
Options under this group are used to configure WSGI (Web Server Gateway
Interface). WSGI is used to serve API requests.    
'''
)

WSGI_ALL_OPTS = [
    cfg.StrOpt(
        "api_paste_config",
        default="/etc/hamal/api-paste.ini",
        help="File name for the paste deploy config for hamal-api."
    ),
    cfg.IntOpt(
        "tcp_keepidle",
        default=600,
        help="Sets the value of TCP_KEEPIDLE in seconds for each "
             "server socket. Not supported on OS X."
    ),
    cfg.BoolOpt(
        "use_ssl",
        default=False,
        help="Set True to enable security connect."
    ),
    cfg.StrOpt(
        "ssl_ca_file",
        default=None,
        help="CA certificate file to use to verify connecting clients."
    ),
    cfg.StrOpt(
        "ssl_cert_file",
        default=None,
        help="Certificate file to use when starting the server securely."
    ),
    cfg.StrOpt(
        "ssl_key_file",
        default=None,
        help="Private key file to use when starting the server securely."
    ),
    cfg.IntOpt(
        'max_header_line',
        default=16384,
        help="Maximum line size of message headers to be accepted."
    ),
    cfg.IntOpt(
        "client_socket_timeout",
        default=900,
        help="Timeout for client connections\' socket operations. "
             "If an incoming connection is idle for this number of "
             "seconds it will be closed. A value of \'0\' means "
             "wait forever."
    ),
    cfg.BoolOpt(
        "wsgi_keep_alive",
        default=True,
        help="If False, closes the client socket connection explicitly. "
             "Setting it to True to maintain backward compatibility. "
             "Recommended setting is set it to False."
    ),
    cfg.IntOpt(
        "wsgi_default_pool_size",
        default=1000,
        help="The default value of pool for GreenPool."
    )
]


def register_opts(conf):
    conf.register_group(wsgi_group)
    conf.register_opts(WSGI_ALL_OPTS, group=wsgi_group)


def list_opts():
    return { wsgi_group: WSGI_ALL_OPTS }
