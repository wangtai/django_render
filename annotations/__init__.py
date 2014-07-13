#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last modified: Wang Tai (i@wangtai.me)

"""
url注解
"""

__revision__ = '0.1'

from url_refactor import _Type, _RequestMethod, _M
from url_refactor import _login_required, _get, _post, _url, _param


Type = _Type
Request = _RequestMethod
M = _M
login_required = _login_required
get = _get
post = _post
url = _url
param = _param

global_read_user_interceptor = None
global_access_secret_key = None
global_login_page = None