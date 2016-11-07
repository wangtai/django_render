#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last modified: Wang Tai (i@wangtai.me)

"""
url注解
"""
from .url_refactor import _Type, _RequestMethod
from .url_refactor import _login_required, _get, _post, _url, _files

__revision__ = '0.1'

__all__ = (
    'Type',
    'M',
    'RequestMethod',
    'login_required',
    'get',
    'post',
    'url',
    'files',
    "GET",
)

import functools

Type = _Type
RequestMethod = _RequestMethod
M = _RequestMethod
login_required = _login_required
get = _get
post = _post
url = _url
files = _files

# HTTP请求方法装饰器
# methods = ("GET", "POST")
# for method in methods:
#    setattr(__builtin__, method, functools.partial(_url, method=method))


GET = functools.partial(_url, method=M.GET)
POST = functools.partial(_url, method=M.POST)
PUT = functools.partial(_url, method=M.PUT)
HEAD = functools.partial(_url, method=M.HEAD)
TRACE = functools.partial(_url, method=M.TRACE)
DELETE = functools.partial(_url, method=M.DELETE)
OPTIONS = functools.partial(_url, method=M.OPTIONS)

Params = _get
Fields = _post
