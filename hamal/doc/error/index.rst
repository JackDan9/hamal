========================
OpenStack Compute (nova)
========================

What is nova?
=============

Nova is the OpenStack project that provides a way to provision compute
instances (aka virtual servers). Nova supports creating virtual machines,
baremetal servers (through the use of ironic), and has limited support for
system containers. Nova runs as a set of daemons on top of existing Linux
servers to provide that service.

It requires the following additional OpenStack services for basic function:

* :keystone-doc:`Keystone <>`: This provides identity and authentication for
  all OpenStack services.
* :glance-doc:`Glance <>`: This provides the compute image repository. All
  compute instances launch from glance images.
* :neutron-doc:`Neutron <>`: This is responsible for provisioning the virtual
  or physical networks that compute instances connect to on boot.
* :placement-doc:`Placement <>`: This is responsible for tracking inventory of
  resources available in a cloud and assisting in choosing which provider of
  those resources will be used when creating a virtual machine.

It can also integrate with other services to include: persistent block
storage, encrypted disks, and baremetal compute instances.

For End Users
=============

As an end user of nova, you'll use nova to create and manage servers with
either tools or the API directly.

.. # NOTE(amotoki): toctree needs to be placed at the end of the secion to
   # keep the document structure in the PDF doc.
.. toctree::
   :hidden:

   user/index

Tools for using Nova
--------------------

'''
class OpenstackMigrationSourceMap(BASE, HamalDBBase):
    """Hamal openstack migration sourcemap"""

    __tablename__ = 'openstack_migration_sourcemap'

    source_type = Column(String(64))
    src_source_id = Column(String(64))
    dest_source_id = Column(String(64))

sqlalchemy 的model需要设置一个primary_key的属性
Traceback (most recent call last):
  File "/root/hamal/.venv/bin/hamal-api", line 6, in <module>
    from hamal.cmd.api import main
  File "/root/hamal/.venv/lib/python2.7/site-packages/hamal/cmd/api.py", line 11, in <module>
    from hamal import config
  File "/root/hamal/.venv/lib/python2.7/site-packages/hamal/config.py", line 8, in <module>
    from hamal.db import api as db_api
  File "/root/hamal/.venv/lib/python2.7/site-packages/hamal/db/api.py", line 24, in <module>
    from hamal.db import models
  File "/root/hamal/.venv/lib/python2.7/site-packages/hamal/db/models.py", line 107, in <module>
    class OpenstackMigrationSourceMap(BASE, HamalDBBase):
  File "/root/hamal/.venv/lib/python2.7/site-packages/sqlalchemy/ext/declarative/api.py", line 75, in __init__
    _as_declarative(cls, classname, cls.__dict__)
  File "/root/hamal/.venv/lib/python2.7/site-packages/sqlalchemy/ext/declarative/base.py", line 131, in _as_declarative
    _MapperConfig.setup_mapping(cls, classname, dict_)
  File "/root/hamal/.venv/lib/python2.7/site-packages/sqlalchemy/ext/declarative/base.py", line 160, in setup_mapping
    cfg_cls(cls_, classname, dict_)
  File "/root/hamal/.venv/lib/python2.7/site-packages/sqlalchemy/ext/declarative/base.py", line 194, in __init__
    self._early_mapping()
  File "/root/hamal/.venv/lib/python2.7/site-packages/sqlalchemy/ext/declarative/base.py", line 199, in _early_mapping
    self.map()
  File "/root/hamal/.venv/lib/python2.7/site-packages/sqlalchemy/ext/declarative/base.py", line 696, in map
    self.cls, self.local_table, **self.mapper_args
  File "<string>", line 2, in mapper
  File "<string>", line 2, in __init__
  File "/root/hamal/.venv/lib/python2.7/site-packages/sqlalchemy/util/deprecations.py", line 128, in warned
    return fn(*args, **kwargs)
  File "/root/hamal/.venv/lib/python2.7/site-packages/sqlalchemy/orm/mapper.py", line 716, in __init__
    self._configure_pks()
  File "/root/hamal/.venv/lib/python2.7/site-packages/sqlalchemy/orm/mapper.py", line 1397, in _configure_pks
    % (self, self.persist_selectable.description)
sqlalchemy.exc.ArgumentError: Mapper mapped class OpenstackMigrationSourceMap->openstack_migration_sourcemap could not assemble any primary key columns for mapped table 'openstack_migration_sourcemap'
'''