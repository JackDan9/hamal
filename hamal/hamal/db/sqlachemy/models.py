# Copyright (c) 2011 X.commerce, a business unit of eBay Inc.
# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# Copyright 2011 Piston Cloud Computing, Inc.
# All Rights Reserved.
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
"""
SQLAlchemy models for hamal data.
"""

from oslo_config import cfg
from oslo_utils import timeutils
from oslo_db.sqlalchemy import models
from sqlalchemy import Boolean, Text
from sqlalchemy import (Column, DateTime, String, Integer, schema)
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

from hamal.db import sql


BASE = declarative_base()
ARGS = {'mysql_charset': "utf8"}


def MediumText():
    return Text().with_variant(MEDIUMTEXT(), 'mysql')


class HamalBase(models.TimestampMixin, models.ModelBase):
    metadata = None

    def __copy__(self):
        """Implement a safe copy.copy()
        
        SQLAlchemy-mapped objects travel with an object 
        called an InstanceState, which is paged to that object. It's 
        specifically and tracks everything about that object. It's 
        critical within all attribute operations, including gets 
        and deferred loading. This object definitely cannot be shared among two instances, and must be handled.

        The copy routine here makes use of session.merge() which 
        already essentially implements a "copy" style of operation, 
        which produces a new instance with a new InstanceState and copies 
        all the data along mapped attributes without using any SQL.

        The mode we are using here has the caveat that the given object 
        must be "clean", e.g. that it has no database-loaded state
        that has been updated and not flushed. This is a good thing,
        as creating a copy of an object including non-flushed, pending 
        database state is probably not a good idea; neither represents 
        what the actual row looks like, and only one should be flushed. 
        
        """
        session - orm.Session()

        copy = session.merge(self, load=False)
        return copy


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


class User(BASE):
    """user table"""

    __tablename__ = 'user'

    id = Column(String(64), primary_key=True)
    extra = Column(sql.JsonBlob)
    enabled = Column('enabled', Boolean)
    default_project_id = Column(String(64))
    email = Column(String(255))


class LocalUser(BASE):
    """local user table"""

    __tablename__ = 'local_user'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(64))
    domain_id = Column(String(64))
    name = Column(String(255))


class Password(BASE):
    """password table"""

    __tablename__ = 'password'

    id = Column(Integer, primary_key=True)
    local_user_id = Column(Integer)
    password = Column(String(128))


# Todo(jackdan): every task under the same vcenter will
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
