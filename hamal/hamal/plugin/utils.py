# Copyright 2020 Hamal, Inc.

from dateutil import tz
from datetime import datetime, timedelta

from oslo_log import log as logging

from hamal.exception import HamalException


LOG = logging.getLogger(__name__)


def transfer_datetime(utc_datetime):
    """Change the source datetiem to the localtime"""

    from_datetime_zone = tz.gettz('UTC')
    to_datetime_zone = tz.gettz('CST')
 
    utc_datetime = datetime.strptime(utc_datetime,"%Y-%m-%dT%H:%M:%SZ")
    
    utc = utc_datetime.replace(tzinfo=from_datetime_zone)

    cst_datetime_zone = utc.astimezone(to_datetime_zone)

    cst_datetime = datetime.strftime(cst_datetime_zone, "%Y-%m-%d %H:%M:%S")

    return cst_datetime