# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# Copyright 2012 Red Hat, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
import sys

from oslo_config import cfg

ALL_OPTS = [
    cfg.StrOpt('pybasedir',
        default=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')),
        sample_default='<Path>',
        help="""
The directory where the Hamal python modules are installed.

This directory is used to store template files for networking and remote
console access. It is also the default path for other config options which
need to persist Hamal internal data. It is very unlikely that you need to 
change this option from its default value.

Possible values:

* The full path to to a directory.

Related options:

* ``state_path``
"""),
    cfg.StrOpt('bindir',
        default=os.path.join(sys.prefix, 'local', 'bin'),
        help="""
The directory where the Hamal binaries are installed.

This option is only relevant if the networking capabilities from Hamal are
used (see services below). Hamal's networking capabilities are targeted to be fully replaced by 
""")
]