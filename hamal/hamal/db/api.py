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

"""Defines interface for DB access.

Functions in this module are imported into the hamal.db namespace. Call these
functions from hamal.db namespace, not the hamal.db.api namespace.

All functions in this module return objects that implement a dictionary-like
interface. Currently, many of these objects are sqlalchemy objects that
implement a dictionary interface. However, a future goal is to have all of
these objects be simple dictionaries.

"""


import threading

from oslo_db import exception as db_exc
from oslo_db import options
from oslo_db import concurrency
from oslo_db.sqlalchemy import session as db_session
from oslo_log import log as logging

import hamal.conf
from hamal.db import constants
from hamal.db.sqlachemy import models
from hamal.db.models import BASE
from hamal.i18n import _
from hamal.auth import password_hashing

CONF = hamal.conf.CONF

# NOTE(jackdan): These constants are re-defined in this module to preserve
# existing references to them.
MAX_INT = constants.MAX_INT
SQL_SP_FLOAT_MAX = constants.SQL_SP_FLOAT_MAX

_BACKEND_MAPPING = {'sqlalchemy': 'hamal.db.sqlalchemy.api'}

IMPL = concurrency.TpoolDbapiWrapper(CONF, backend_mapping=_BACKEND_MAPPING)

LOG = logging.getLogger(__name__)


# ###################


# def constraint(**conditions):
#     """Return a constraint object suitable for use with some updates"""
#     return IMPL.constraint(**conditions)


# def equal_any(*values):
#     """Return an equality condition object suitable for use in a constraint, 
    
#     Equal_any conditions require that a model object's attribute equal any 
#     one of the given values.
#     """
#     return IMPL.equal_any(*values)


# def not_equal(*values):
#     """Return an inequality condition object suitable for use in a constraint.
    
#     Not_equal conditions require that a model object's attribute differs from 
#     all of the given values.
#     """
#     return IMPL.not_equal(*values)


# #####################


# def select_db_reader_mode(f):
#     """Decorator to select synchronous or asynchronous reader mode.
    
#     The kwarg argument 'use_slave' defines reader mode. Asynchronous reader
#     will be used if 'use_slave' is True and synchronous reader otherwise.
#     """
#     return IMPL.select_db_reader_mode(f)


# #####################


# def service_destroy(context, service_id):
#     """Destroy the service or raise if it does not exist."""
#     return IMPL.service_destroy(context, service_id)


# def service_get(context, service_id):
#     """Get a service or raise if it does not exist."""
#     return IMPL.service_get(context, service_id)


# def service_get_by_uuid(context, service_uuid):
#     """Get a service by it's uuid or raise ServiceNotFound if it does not exist."""
#     return IMPL.service_get_by_uuid(context, service_uuid)


# def service_get_minimum_version(context, binary):
#     """Get the minimum service version in the database."""
#     return IMPL.service_get_minimum_version(context, binary)


# def service_get_by_host_and_topic(context, host, topic):
#     """Get a service by hostname and topic it listens to."""
#     return IMPL.service_get_by_host_and_topic(context, host, topic)


# def service_get_by_host_and_binary(context, host, binary):
#     """Get a service by hostname and binary it listens to."""
#     return IMPL.service_get_by_host_and_binary(context, host, binary)


# def service_get_all(context, disabled=None):
#     """Get all services."""
#     return IMPL.service_get_all(context, disabled)


# def service_get_all_by_topic(context, topic):
#     """Get all services for a given topic."""
#     return IMPL.service_get_all_by_topic(context, topic)


# def service_get_all_by_binary(context, binary, include_disabled=False):
#     """Get services for a given binary.
    
#     Includes disabled services if 'include_disabled' parameter is True
#     """
#     return IMPL.service_get_all_by_binary(context, binary, 
#                                           include_disabled=include_disabled)


# options.set_defaults(CONF, connection='mysql+pymysql://root:passw0rd@127.0.0.1/hamal')

_LOCK = threading.Lock()
_FACADE = None


def _create_facade_lazily():
    global _LOCK
    with _LOCK:
        global _FACADE
        if _FACADE is None:
            _FACADE = db_session.EngineFacade(
                CONF.database.connection,
                **dict(CONF.database)
            )
        return _FACADE


def get_engine():
    facade = _create_facade_lazily()
    return facade.get_engine()


def get_session(**kwargs):
    facade = _create_facade_lazily()
    return facade.get_session(**kwargs)


def dispose_engine():
    get_engine().dispose()


def is_user_context(context):
    """Indicates if the request context is a normal user."""
    if not context:
        return False
    if context.is_admin:
        return False
    if not context.user_id or not context.project_id:
        return False
    return True


def register_models():
    # NOTE(lhx): register all models before invoking db api functions
    engine = get_engine()
    BASE.metadata.create_all(engine)


def unregister_models():
    engine = get_engine()
    BASE.metadata.drop_all(engine)


def model_query(context, model, *args, **kwargs):
    """Query helper that accounts for context's `read_deleted` field.

    :param context: context to query under
    :param session: if present, the session to use
    :param read_deleted: if present, overrides context's read_deleted field.
    """
    session = kwargs.get('session') or get_session()
    read_deleted = kwargs.get('read_deleted') or context.read_deleted

    query = session.query(model, *args)

    if read_deleted == 'no':
        query = query.filter_by(deleted=False)
    elif read_deleted == 'yes':
        pass  # omit the filter to include deleted and active
    elif read_deleted == 'only':
        query = query.filter_by(deleted=True)
    elif read_deleted == 'int_no':
        query = query.filter_by(deleted=0)
    else:
        raise Exception(
            _("Unrecognized read_deleted value '%s'") % read_deleted)

    return query


#########################


def register(uuid, name, password, email, enabled=1):
    session = get_session()
    auth_models = models.Auth(id=uuid,
                              name=name,
                              password=password,
                              email=email,
                              enabled=enabled)
    try:
        with session.begin():
            session.add(auth_models)
    except db_exc.DBDuplicateEntry:
        raise
    return auth_models


def auth(username, password):
    """authenticate user information,

    :param username: context to username
    :param string: context to password
    """
    session = get_session()
    query = session.query(models.User)
    local_user_query = session.query(models.LocalUser)
    password_query = session.query(models.Password)
    
    # user information
    user = query.filter_by(email=username).first()
    
    # local user information
    local_user_id = user.id
    local_user = local_user_query.filter_by(user_id=local_user_id).first()
    
    # user password information
    user_password_id = local_user.id
    user_password = password_query.filter_by(local_user_id=user_password_id).first()

    # verify user password
    hash_password = password_hashing.verify_password(password, user_password.password)
    
    if user is None or not hash_password:
        return None
    else:
        return user


def task_get_all():
    session = get_session()
    tasks = session.query(models.Tasks).all()
    return tasks


def openstack_task_get_all():
    session = get_session()
    openstack_tasks = session.query(models.OpenstackTasks).all()
    return openstack_tasks


def task_get_by_uuid(uuid):
    session = get_session()
    query = session.query(models.Tasks)
    task = query.filter_by(id=uuid).first()
    return task


def openstack_task_get_by_uuid(uuid):
    session = get_session()
    query = session.query(models.OpenstackTasks)
    openstack_task = query.filter_by(id=uuid).first()
    return openstack_task


def task_get_by_state_init(init):
    session = get_session()
    query = session.query(models.Tasks)
    task = query.filter_by(state=init).first()
    return task


def openstack_task_get_by_state_init(init):
    session = get_session()
    query = session.query(models.OpenstackTasks)
    openstack_task = query.filter_by(state=init).first()
    return openstack_task
 

def task_create(uuid, name, vc, user, pwd, uri, osp_network, osp_flavor, osp_storage, osp_hamal_type, state, percent=0):
    """The value of state could be init or converting

    if one converting task is failed or succeed, we
    will move it to the task_history table.
    """
    session = get_session()
    task_models = models.Tasks(id=uuid,
                               name=name,
                               vcenter=vc,
                               user=user,
                               pwd=pwd,
                               uri=uri,
                               osp_network=osp_network,
                               osp_flavor=osp_flavor,
                               osp_storage=osp_storage,
                               osp_hamal_type=osp_hamal_type,
                               state=state,
                               percent=percent)
    try:
        with session.begin():
            session.add(task_models)
    except db_exc.DBDuplicateEntry:
        raise
    return task_models


def openstack_task_create(uuid, name, auth_url, user, pwd, osp_network, osp_flavor, osp_storage, osp_hamal_type, state, percent=0):
    """The value of state could be init or converting

    if one converting openstack_task is failed or succeed, we
    will move it to the openstack_task_history table.
    """
    session = get_session
    openstack_task_models = models.OpenstackTasks(id=uuid,
                                                  name=name,
                                                  auth_url=auth_url,
                                                  user=user,
                                                  pwd=pwd,
                                                  osp_network=osp_network,
                                                  osp_flavor=osp_flavor,
                                                  osp_storage=osp_storage,
                                                  osp_hamal_type=osp_hamal_type,
                                                  state=state,
                                                  percent=percent)
    try:
        with session.begin():
            session.add(openstack_task_models)
    except db_exc.DBDuplicateEntry:
        raise
    return openstack_task_models


def task_update_state_by_uuid(uuid, state):
    session = get_session()
    with session.begin():
        query = session.query(models.Tasks)
        task = query.filter_by(id=uuid).first()
        task.state = state
    return task


def openstack_task_update_state_by_uuid(uuid, state):
    session = get_session()
    with session.begin():
        query = session.query(models.OpenstackTasks)
        openstack_task = query.filter_by(id=uuid).first()
        openstack_task.state = state
    return openstack_task        


def task_update_percent_by_uuid(uuid, percent=0):
    session = get_session()
    with session.begin():
        query = session.query(models.Tasks)
        task = query.filter_by(id=uuid).first()
        task.percent = percent
    return task


def openstack_update_percent_by_uuid(uuid, percent=0):
    session = get_session()
    with session.begin():
        query = session.query(models.OpenstackTasks)
        openstack_task = query.filter_by(id=uuid).first()
        openstack_task.percent = percent
    return openstack_task


def task_delete_by_uuid(uuid):
    session = get_session()
    with session.begin():
        query = session.query(models.Tasks)
        task = query.filter_by(id=uuid).first()
        if task is not None:
            session.delete(task)
            #session.commit()
            #task.delete()


def openstack_task_delete_by_uuid(uuid):
    session = get_session()
    with session.begin():
        query = session.query(models.OpenstackTasks)
        openstack_task = query.filter_by(id=uuid).first()
        if openstack_task is not None:
            session.delete(openstack_task)


def task_history_get_all():
    session = get_session()
    histories = session.query(models.TaskHistory).all()
    return histories


def openstack_task_histories_get_all():
    session = get_session()
    histories = session.query(models.OpenstackTaskHistory).all()
    return histories


def task_history_get_by_uuid(uuid):
    session = get_session()
    query = session.query(models.TaskHistory)
    history = query.filter_by(id=uuid).first()
    return history


def openstack_task_history_get_by_uuid(uuid):
    session = get_session()
    query = session.query(models.OpenstackTasks)
    openstack_task_history = query.filter_by(id=uuid).first()
    return openstack_task_history


def task_history_get_by_all_succeed():
    session = get_session()
    query = session.query(models.TaskHistory)
    succeed_histories = query.filter_by(state='succeed').all()
    return succeed_histories


def openstack_task_history_get_by_all_succeed():
    session = get_session()
    query = session.query(models.OpenstackTasksHistory)
    openstack_task_succeed_histories = query.filter_by(state='succeed').all()
    return openstack_task_succeed_histories


def task_history_create(uuid, name, vc, user, pwd, uri, osp_network, osp_flavor, osp_storage, osp_hamal_type, state):
    """The value of state could be failed or succeed"""
    session = get_session()
    history_models = models.TaskHistory(id=uuid,
                                        name=name,
                                        vcenter=vc,
                                        user=user,
                                        pwd=pwd,
                                        uri=uri,
                                        osp_network=osp_network,
                                        osp_flavor=osp_flavor,
                                        osp_storage=osp_storage,
                                        osp_hamal_type=osp_hamal_type,
                                        state=state)
    try:
        with session.begin():
            session.add(history_models)
    except db_exc.DBDuplicateEntry:
        raise
    return history_models


def openstack_task_history_create(uuid, name, auth_url, user, pwd, osp_network, osp_flavor, osp_storage, osp_hamal_type, state):
    """The value of state could be failed or succeed"""
    session = get_session()
    openstack_history_models = models.OpenstackTaskHistory(id=uuid,
                                                           name=name,
                                                           auth_url=auth_url,
                                                           user=user,
                                                           pwd=pwd,
                                                           osp_network=osp_network,
                                                           osp_flavor=osp_flavor,
                                                           osp_storage=osp_storage,
                                                           osp_hamal_type=osp_hamal_type,
                                                           state=state)
    try:
        with session.begin():
            session.add(openstack_history_models)
    except db_exc.DBDuplicateEntry:
        raise
    return openstack_history_models


def task_history_update_state_by_uuid(uuid, state):
    session = get_session()
    with session.begin():
        query = session.query(models.TaskHistory)
        history = query.filter_by(id=uuid).first()
        history.state = state
    return history


def openstack_task_history_update_state_by_uuid(uuid, state):
    session = get_session()
    with session.begin():
        query = session.query(models.OpenstackTaskHistory)
        openstack_history = query.filter_by(id=uuid).first()
        openstack_history.state = state
    return openstack_history


def task_history_delete_by_uuid(uuid):
    session = get_session()
    with session.begin():
        query = session.query(models.TaskHistory)
        history = query.filter_by(id=uuid).first()
        if history is not None:
            session.delete(history)


def openstack_task_history_delete_by_uuid(uuid):
    session = get_session()
    with session.begin():
        query = session.query(models.OpenstackTaskHistory)
        openstack_history = query.filter_by(id=uuid).first()
        if openstack_history is not None:
            session.delete(openstack_history)


###########

def license_get():
    session = get_session()
    query = session.query(models.License)
    license = query.all()
    try:
        return license[0]
    except IndexError:
        return license


def license_create(**kwargs):
    session = get_session()
    license_models = models.License(license=kwargs.get('license'))
    try:
        with session.begin():
            session.add(license_models)
    except Exception:
        raise
    return license_models


def license_update(**kwargs):
    session = get_session()
    with session.begin():
        query = session.query(models.License)
        license = query.all()[0]
        license.license = kwargs.get('license')
        license.expired = kwargs.get('expired')
    return license
