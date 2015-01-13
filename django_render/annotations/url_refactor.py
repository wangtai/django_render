#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last modified: Wang Tai (i@wangtai.me)

"""
方法定义
"""
import logging

from enum import Enum, enum


__revision__ = '0.1'

import sys
import functools
import json

from django.conf.urls import url as django_url, patterns
from django.http import HttpResponse, HttpResponseRedirect, Http404

from django_render import global_read_user_interceptor, global_access_secret_key, global_login_page


CONTENT_TYPE_JSON = 'application/json'


class _Type(Enum):
    str_list = 0
    int_list = 1
    json = 2
    file = 3


class _RequestMethod:
    def __init__(self):
        pass

    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    HEAD = 'HEAD'
    TRACE = 'TRACE'
    DELETE = 'DELETE'
    OPTIONS = 'OPTIONS'


_M = _RequestMethod


def _login_required(is_ajax=False, access_secret_key=None, read_user_interceptor=None, login_page=None,
                    check_auth=None):
    def paramed_decorator(func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            if is_ajax:
                response = HttpResponse(json.dumps({'rt': False, 'message': 'login first'}),
                                        content_type=CONTENT_TYPE_JSON)
            else:
                response = HttpResponseRedirect(login_page)
            request = args[0]
            if (hasattr(request, 'user') and request.user.is_authenticated()) \
                    or access_secret_key == request.GET.get('access_secret_key', ''):
                return func(*args, **kwargs)
            user = read_user_interceptor(request)
            if user is None:
                return response
            else:
                if check_auth is not None:
                    if check_auth(request, user):
                        pass
                    else:
                        return HttpResponse(json.dumps({'rt': False, 'message': 'Permission Denied!'}),
                                            content_type=CONTENT_TYPE_JSON)
                if 'user' in func.func_code.co_varnames:
                    kwargs.update({'user': user})
            return func(*args, **kwargs)

        return decorated

    if read_user_interceptor is None:
        if global_read_user_interceptor is not None:
            read_user_interceptor = global_read_user_interceptor
        else:
            read_user_interceptor = lambda request: None

    if access_secret_key is None:
        if global_access_secret_key is not None:
            access_secret_key = global_access_secret_key

    if login_page is None:
        if global_login_page is not None:
            login_page = global_login_page
        else:
            login_page = 'login'

    return paramed_decorator


def __param(method_name, *p_args, **p_kwargs):
    """
    @get('param1', 'param2')
    @get(param1={'name':'parameter_name', 'type':int, 'default':0})
    @get(param1={'type':int, 'default':0})
    @get(param1={'type':int })
    @get(param1=('param_name', int, 0))
    @get(param1=(int, 0))
    @get(param1=int)
    """

    def paramed_decorator(func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            request = args[0]
            m = {'get': request.GET, 'post': request.POST, 'param': request.REQUEST}
            method = m[method_name]
            for k, v in p_kwargs.items():
                _name = None
                _type = None
                _default = None

                # logging.debug(v)
                if type(v) == str:
                    _type = str
                    _name = v
                elif type(v) == dict:
                    if 'name' in v:
                        _name = v['name']
                    if 'type' in v:
                        _type = v['type']
                    if 'default' in v:
                        _default = v['default']
                elif type(v) == tuple and len(v) == 3:
                    _name = v[0]
                    _type = v[1]
                    _default = v[2]
                elif type(v) == tuple and len(v) == 2:
                    _type = v[0]
                    _default = v[1]
                elif type(v) == type:
                    _type = v
                elif v in (_Type.str_list, _Type.int_list, _Type.json, _Type.file):
                    _type = v

                if _name is None:
                    _name = k
                if _type is None:
                    _type = str

                has_key = True
                try:
                    if _type == _Type.file:
                        if method_name != 'post':
                            return HttpResponse(
                                json.dumps({'rt': False,
                                            'message': "The file parameter <{}> should in POST method".format(_name)}),
                                content_type=CONTENT_TYPE_JSON)
                        origin_v = request.FILES[_name]
                    else:
                        origin_v = ','.join(method.getlist(_name)).encode('utf-8').strip()
                        if len(origin_v) == 0:
                            has_key = False
                except KeyError:
                    has_key = False

                if has_key:
                    if _type == bool:
                        origin_v = origin_v.lower()
                        if origin_v == 'false' or origin_v == '0' or origin_v == 'off':
                            value = False
                        elif origin_v == 'true' or origin_v == 'on':
                            value = True
                        else:
                            value = bool(origin_v)
                    elif _type == _Type.str_list:
                        value = [item for item in origin_v.split(',') if len(item) > 0]
                    elif _type == _Type.int_list:
                        value = [int(item) for item in origin_v.split(',')]
                    elif _type == _Type.json:
                        try:
                            value = json.loads(origin_v)
                        except ValueError:
                            return HttpResponse(
                                json.dumps({'rt': False, 'message': "No JSON object could be decoded"}),
                                content_type=CONTENT_TYPE_JSON)
                    elif _type == _Type.file:
                        value = origin_v
                        pass
                    else:
                        value = _type(origin_v)
                else:
                    if _default is not None:
                        value = _default
                    else:
                        return HttpResponse(
                            json.dumps({'rt': False, 'message': 'Please specify the parameter : ' + _name + ";"}),
                            content_type=CONTENT_TYPE_JSON)
                kwargs.update({k: value})

            for k in p_args:
                try:
                    kwargs.update({k: method[k].encode('utf-8')})
                except KeyError:
                    return HttpResponse(json.dumps({'rt': False, 'message': 'Please specify the parameter : ' + k}),
                                        content_type=CONTENT_TYPE_JSON)
            return func(*args, **kwargs)

        return decorated

    return paramed_decorator


def _get(*p_args, **p_kwargs):
    """
    @get('param1', 'param2')
    @get(param1={'name':'parameter_name', 'type':int, 'default':0})
    @get(param1={'type':int, 'default':0})
    @get(param1={'type':int })
    @get(param1=('param_name', int, 0))
    @get(param1=(int, 0))
    @get(param1=int)
    """
    return __param('get', *p_args, **p_kwargs)


def _post(*p_args, **p_kwargs):
    """
    @post('param1', 'param2')
    @post(param1={'name':'parameter_name', 'type':int, 'default':0})
    @post(param1={'type':int, 'default':0})
    @post(param1={'type':int })
    @post(param1=('param_name', int, 0))
    @post(param1=(int, 0))
    @post(param1=int)
    """
    return __param('post', *p_args, **p_kwargs)


def _files(*p_args, **p_kwargs):
    """

    :param p_args:
    :param p_kwargs:
    :return:
    """

    def paramed_decorator(func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            request = args[0]
            for file_name in p_args:
                fp = request.FILES.get(file_name, None)

                try:
                    kwargs.update({file_name: fp})
                except ValueError:
                    return HttpResponse(
                        json.dumps({'rt': False, 'message': 'Please specify the parameter : ' + file_name}),
                        content_type=CONTENT_TYPE_JSON)
                except KeyError:
                    return HttpResponse(
                        json.dumps({'rt': False, 'message': 'Please specify the parameter : ' + file_name}),
                        content_type=CONTENT_TYPE_JSON)

            return func(*args, **kwargs)

        return decorated

    return paramed_decorator


def _param(*p_args, **p_kwargs):
    return __param('param', *p_args, **p_kwargs)


url_mapping = {}


def url_dispatch(request, *args, **kwargs):
    # expect_method = kwargs.pop('expect_method', None)
    # logging.debug(url_mapping)
    url_pattern = kwargs.pop('url_pattern', None)
    is_json = kwargs.pop('is_json', False)
    method_mapping = url_mapping.get(url_pattern, None)
    if method_mapping is None:
        raise Http404
    view = method_mapping.get(request.method, None)
    # logging.debug(view)
    if view is not None:
        rt = view(request, *args, **kwargs)
        logging.debug(type(rt))
        is_json = is_json or not issubclass(type(rt), HttpResponse)
        logging.debug(is_json)
        if is_json:
            return json_result(rt)
        return rt
    else:
        return HttpResponse(status=403, content="Request Forbidden 403")


def _url(url_pattern, method=None, is_json=False, *p_args, **p_kwargs):
    if method is None:
        method = [_M.POST, _M.GET]

    def paramed_decorator(func):
        @functools.wraps(func)
        def decorated(self, *args, **kwargs):
            return func(self, *args, **kwargs)

        url_key = func.__module__ + url_pattern
        mapping = url_mapping.get(url_key, None)
        if mapping is None:
            url_mapping.update({url_key: {}})

        if type(method) in (list, tuple, set):
            for m in method:
                url_mapping[url_key].update({m: decorated})
        else:
            url_mapping[url_key].update({method: decorated})

        module = sys.modules[func.__module__]
        if not hasattr(module, 'urlpatterns'):
            module.urlpatterns = patterns('', )

        module.urlpatterns += \
            patterns('', django_url(url_pattern, url_dispatch,
                                    {'url_pattern': url_key, 'is_json': is_json}, *p_args,
                                    **p_kwargs), )
        return decorated

    return paramed_decorator


def json_result(rt):
    response = HttpResponse(content_type=CONTENT_TYPE_JSON)
    if type(rt) == tuple:
        status = rt[0]
        if status:  # return True, {}
            rt_obj = {'rt': status}
            rt_obj.update(rt[1])
            response.content = json.dumps(rt_obj)
            return response
        else:  # return False, 'message'
            if isinstance(rt[1], enum.Enum) or isinstance(rt[1], Enum):
                response.content = json.dumps({'rt': status, 'message': rt[1].value})
            else:
                response.content = json.dumps({'rt': status, 'message': rt[1]})
            return response
    elif type(rt) is bool:  # return True / return False
        response.content = json.dumps({'rt': rt, 'message': ''})
        return response
    elif type(rt) is dict:  # return {}
        response.content = json.dumps(rt)
        return response
    elif type(rt) is list:  # return []
        response.content = json.dumps(rt)
        return response
    elif type(rt) is HttpResponse:  # return {}
        response = rt
        return response
    elif rt is None:  # direct return
        response.content = json.dumps({})
        return response
    else:
        response.content = json.dumps({'message': str(rt)})
        return response


