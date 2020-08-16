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

from hamal.conf import api
from hamal.conf import database
from hamal.conf import engine
from hamal.conf import exception
from hamal.conf import extension
from hamal.conf import identity
from hamal.conf import rpc
from hamal.conf import wsgi
from hamal.conf import server
from hamal.conf import vmware_rsa_license
from hamal.conf import cli
from hamal.conf import token
from hamal.conf import source_cluster
from hamal.conf import destination_cluster


CONF = cfg.CONF


api.register_opts(CONF)
database.register_opts(CONF)
engine.register_opts(CONF)
exception.register_opts(CONF)
extension.register_opts(CONF)
rpc.register_opts(CONF)
wsgi.register_opts(CONF)
identity.register_opts(CONF)
server.register_opts(CONF)
vmware_rsa_license.register_opts(CONF)
cli.register_opts(CONF)
token.register_opts(CONF)
source_cluster.register_opts(CONF)
destination_cluster.register_opts(CONF)


# conf_modules = [
#     api,
#     engine,
#     extension,
#     wsgi
# ]

# CONF = cfg.CONF


# def configure(conf=None):
#     """Register all options of module in conf_modules

#     :param conf: An Object of ConfigOpts in oslo_conf.cfg,
#                  usually is ``cfg.CONF``

#     :returns: None
#     """

#     if conf is None:
#         conf = CONF

#     for module in conf_modules:
#         module.register_opts(conf)


# # Need to invoke configure function to register options
# configure(CONF)
