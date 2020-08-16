# Copyright 2020 Hamal, Inc.

from oslo_config import cfg


vmware_license_group = cfg.OptGroup(name='vmware_rsa_license',
                                    title='VMware License Options')

VMWARE_LICENSE_ALL_OPTS = [
    cfg.StrOpt('private_key_file', 
               default='/etc/hamal/hamal_private.pem'),
    cfg.StrOpt('public_key_file',
               default='/etc/hamal/hamal_public.pem'),
]

def register_opts(conf):
    conf.register_group(vmware_license_group)
    conf.register_opts(VMWARE_LICENSE_ALL_OPTS, group=vmware_license_group)


def list_opts():
    return { vmware_license_group: VMWARE_LICENSE_ALL_OPTS }
