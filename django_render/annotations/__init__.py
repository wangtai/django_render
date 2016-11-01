#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last modified: Wang Tai (i@wangtai.me)

"""
url注解
"""

__revision__ = '0.1'


import functools


from url_refactor import _Type, _RequestMethod, _M
from url_refactor import _login_required, _get, _post, _url, _files, _field, _param


Type = _Type
M = _M
RequestMethod = _RequestMethod
login_required = _login_required
get = _get
post = _post
url = _url
files = _files

# HTTP请求方法装饰器
methods = ("GET", "POST")
for method in methods:
    setattr(__builtin__, method, functools.partial(_url, method=method))

Params = _param
Fields = _field
