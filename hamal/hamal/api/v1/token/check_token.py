# Copyright 2020 Hamal, Inc.

import base64
import functools

import webob.exc


def check_user_token(func):
    pass
    # @functools.wraps(func)
    # def wrapper(*args, **kwargs):
    #     import pdb
    #     pdb.set_trace()