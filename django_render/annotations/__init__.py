#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last modified: Wang Tai (i@wangtai.me)

"""
url注解
"""

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
)

from url_refactor import _Type, _RequestMethod
from url_refactor import _login_required, _get, _post, _url, _files

Type = _Type
RequestMethod = _RequestMethod
M = _RequestMethod
login_required = _login_required
get = _get
post = _post
url = _url
files = _files
