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

from oslo_utils import timeutils
from oslo_db.sqlalchemy import models
from sqlalchemy import Boolean
from sqlalchemy import Column, DateTime, String, Integer, schema
from sqlalchemy.ext.declarative import declarative_base


BASE = declarative_base()
ARGS = {'mysql_charset': "utf8"}


class HamalDBBASE(models.TimestampMixin, models.ModelBase):
    created_at = Column(DateTime, default=timeutils.utcnow)
    updated_at = Column(DateTime, default=timeutils.utcnow,
                        onupdate=timeutils.utcnow)


class Auth(BASE, HamalDBBASE):
    """auth table"""

    __tablename__ = 'auth'

    id = Column(String(36), primary_key=True)
    name = Column(String(128), unique=True, nullable=False)
    password = Column(String(255))
    email = Column(String(255))
    enabled = Column(Boolean, default=1)
    project_id = Column(String(36))  # reserve param for project


# Todo(youqy): every task under the same vcenter will
# cause vcenter/user/pwd/uri duplicate
# we will fixed it in future
class Tasks(BASE, HamalDBBASE):
    """Hamal tasks table"""

    __tablename__ = 'tasks'

    id = Column(String(36), primary_key=True)
    name = Column(String(128), nullable=False)  # vm name
    vcenter = Column(String(255))
    user = Column(String(255))
    pwd = Column(String(255))
    uri = Column(String(255))
    osp_network = Column(String(128))
    osp_flavor = Column(String(128))
    osp_storage = Column(String(128))
    osp_hamal_type = Column(String(36))
    state = Column(String(36))
    percent = Column(Integer)


class OpenstackTasks(BASE, HamalDBBASE):
    """Hamal openstack tasks tabel"""

    __tablename__ = 'openstack_task'

    id = Column(String(36), primary_key=True)
    name = Column(String(128), nullable=False) # instance name
    auth_url = Column(String(255))
    user = Column(String(255))
    pwd = Column(String(255))
    osp_network = Column(String(128))
    osp_flavor = Column(String(128))
    osp_storage = Column(String(128))
    osp_hamal_type = Column(String(36))
    state = Column(String(36))
    percent = Column(Integer)


class TaskHistory(BASE, HamalDBBASE):
    """Hamal history of tasks table"""

    __tablename__ = 'task_history'

    id = Column(String(36), primary_key=True)
    name = Column(String(128), nullable=False)
    vcenter = Column(String(255))
    user = Column(String(255))
    pwd = Column(String(255))
    uri = Column(String(255))
    osp_network = Column(String(128))
    osp_flavor = Column(String(128))
    osp_storage = Column(String(128))
    osp_hamal_type = Column(String(36))
    state = Column(String(36))


class OpenstackTaskHistory(BASE, HamalDBBASE):
    """Hamal openstack history of tasks table"""

    __tablename__ = 'openstack_task_history'

    id = Column(String(36), primary_key=True)
    name = Column(String(128), nullable=False)
    auth_url = Column(String(255))
    user = Column(String(255))
    pwd = Column(String(255))
    osp_network = Column(String(128))
    osp_flavor = Column(String(128))
    osp_storage = Column(String(128))
    osp_hamal_type = Column(String(36))
    state = Column(String(36))


class License(BASE, HamalDBBASE):
    """Hamal license table"""

    __tablename__ = 'license'

    id = Column(Integer, primary_key=True)
    license = Column(String(2048))
    expired = Column(Boolean, default=False)


class OpenstackLicense(BASE, HamalDBBASE):
    """Hamal Openstack license table"""

    __tablename__ = 'openstack_license'

    id = Column(Integer, primary_key=True)
    license = Column(String(2048))
    expired = Column(Boolean, default=False)
