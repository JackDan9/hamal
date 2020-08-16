#!/usr/bin/env python3
# -*- coding:utf-8 -*-x`

"""A Script used for generate a license"""

import sys
from datetime import datetime
from datetime import timedelta

from oslo_config import cfg

from hamal.db import api as db_api
from hamal.utils.crypto_rsa import VMwareRSALicense
import hamal.conf


CONF = hamal.conf.CONF


# Export an existed license, the command is
# ./license [--config-file /etc/hamal/hamal.conf] --mode export --license [exist_license]
def export_license(license):
    has_license = db_api.license_get()
    if not has_license:
        db_api.license_create(license=license)


# Create a new license, the command is
# ./license [--config-file /etc/hamal/hamal.conf] --mode create --servers 10 --days 30
# it just create a new license, you need to export it manual
def create_new_license(servers=None, days=None):
    if days is None:
        days = set_expired_at()
    else:
        days = set_expired_at(days)
    rsa = VMwareRSALicense()
    new_license = rsa.sign_a_license(server_nums=servers, expired_at=days)
    print(new_license)
    return new_license


# Update a new license to db, the command is
# ./license [--config-file /etc/hamal/hamal.conf] --mode update --license [exist_license]
def update_license(license):
    exist_license = db_api.license_get()
    if not exist_license:
        print("There is no license exist, please export one first.")
    else:
        db_api.license_update(license=license)


def set_expired_at(days=6):
    return datetime.utcnow() + timedelta(days=days)


def main():
    import pdb
    pdb.set_trace()
    CONF(sys.argv[1:], 
         project='hamal')
    if CONF.mode[0] == 'create':
        create_new_license(CONF.servers, CONF.days)
    elif CONF.mode[0] == 'export':
        if CONF.license:
            export_license(CONF.license)
        else:
            print("Please use --license to specify an existed license")
    elif CONF.mode[0] == 'update':
        if CONF.license:
            export_license(CONF.license)
        else:
            print("Please use --license to specify an existed license")


if __name__ == '__main__':
    main()
