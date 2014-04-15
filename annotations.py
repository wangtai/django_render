#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last modified: Wang Tai (i@wangtai.me)

"""
url注解
"""

__revision__ = '0.1'

import sys
import functools
import json

from django.conf.urls import url as django_url, patterns
from django.http import HttpResponse, HttpResponseRedirect

from django_render import global_read_user_interceptor, global_access_secret_key, global_login_page


class Type:
    str_list = 'str_list'
    int_list = 'int_list'


class RequestMethod:
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


def login_required(is_ajax=False, access_secret_key=None, read_user_interceptor=None, login_page=None):
    def paramed_decorator(func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            if is_ajax:
                response = HttpResponse(json.dumps({'rt': False, 'message': 'login first'}),
                                        content_type='application/json')
            else:
                response = HttpResponseRedirect(login_page)
            request = args[0]
            if (hasattr(request, 'user') and request.user.is_authenticated()) \
                    or access_secret_key is request.GET.get('access_secret_key', ''):
                return func(*args, **kwargs)
            user = read_user_interceptor(request)
            if user is None:
                return response
            else:
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


def _param(method_name, *p_args, **p_kwargs):
    '''
    @get('param1', 'param2')
    @get(param1={'name':'parameter_name', 'type':int, 'default':0})
    @get(param1={'type':int, 'default':0})
    @get(param1={'type':int })
    @get(param1=('param_name', int, 0))
    @get(param1=(int, 0))
    @get(param1=int)
    '''

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

                if type(v) == str and v not in (Type.str_list, Type.int_list):
                    _type = str
                    _name = v
                elif type(v) == dict:
                    if v.has_key('name'):
                        _name = v['name']
                    if v.has_key('type'):
                        _type = v['type']
                    if v.has_key('default'):
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

                if _name == None:
                    _name = k
                if _type == None:
                    _type = str

                has_key = True
                try:
                    origin_v = method[_name].encode('utf-8').strip()
                    if len(origin_v) == 0:
                        has_key = False
                except:
                    has_key = False

                if has_key:
                    if _type == bool:
                        origin_v = origin_v.lower()
                        if origin_v == 'false' or origin_v == '0':
                            value = False
                        elif origin_v == 'true':
                            value = True
                        else:
                            value = bool(origin_v)
                    elif _type == Type.str_list:
                        value = [item for item in origin_v.split(',') if len(item) > 0]
                    elif _type == Type.int_list:
                        value = [int(item) for item in origin_v.split(',')]
                    else:
                        value = _type(origin_v)
                else:
                    if _default is not None:
                        value = _default
                    else:
                        return HttpResponse(
                            json.dumps({'rt': False, 'info': 'Please specify the parameter : ' + _name + ";"}))
                kwargs.update({k: value})

            for k in p_args:
                try:
                    kwargs.update({k: method[k].encode('utf-8')})
                except:
                    return HttpResponse(json.dumps({'rt': False, 'info': 'Please specify the parameter : ' + k}))
            return func(*args, **kwargs)

        return decorated

    return paramed_decorator


def get(*p_args, **p_kwargs):
    '''
    @get('param1', 'param2')
    @get(param1={'name':'parameter_name', 'type':int, 'default':0})
    @get(param1={'type':int, 'default':0})
    @get(param1={'type':int })
    @get(param1=('param_name', int, 0))
    @get(param1=(int, 0))
    @get(param1=int)
    '''
    return _param('get', *p_args, **p_kwargs)


def post(*p_args, **p_kwargs):
    '''
    @post('param1', 'param2')
    @post(param1={'name':'parameter_name', 'type':int, 'default':0})
    @post(param1={'type':int, 'default':0})
    @post(param1={'type':int })
    @post(param1=('param_name', int, 0))
    @post(param1=(int, 0))
    @post(param1=int)
    '''
    return _param('post', *p_args, **p_kwargs)


def param(*p_args, **p_kwargs):
    return _param('param', *p_args, **p_kwargs)


def url(url_pattern, *args, **kwargs):
    def paramed_decorator(func):
        @functools.wraps(func)
        def decorated(self, *args, **kwargs):
            return func(self, *args, **kwargs)

        module = sys.modules[func.__module__]
        if not hasattr(module, 'urlpatterns'):
            module.urlpatterns = patterns('', )

        module.urlpatterns += patterns('', django_url(url_pattern, decorated, *args, **kwargs), )
        return decorated

    return paramed_decorator


def req_method(expect_method=RequestMethod.GET, *p_args, **p_kwargs):
    p_kwargs.update({'expect_method': expect_method})

    def paramed_decorator(func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            expect_method = p_kwargs['expect_method']
            request = args[0]
            method = request.META['REQUEST_METHOD']
            if method != expect_method:
                if method == RequestMethod.POST:
                    if 'request_method' in request.GET:
                        expect_method = request.GET['request_method']
            if method != expect_method:
                return HttpResponse(status=403, content="Request Forbidden 403")
            return func(*args, **kwargs)

        return decorated

    return paramed_decorator


def is_json():
    def paramed_decorator(func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            response = HttpResponse(content_type='application/json')
            rt = func(*args, **kwargs)
            if type(rt) == tuple:
                status = rt[0]
                if status:  # return True, {}
                    rt_obj = {'rt': status}
                    rt_obj.update(rt[1])
                    response.content = json.dumps(rt_obj)
                    return response
                else:  # return False, 'message'
                    response.content = json.dumps({'rt': status, 'message': rt[1]})
                    return response
            elif type(rt) is bool:  # return True / return False
                response.content = json.dumps({'rt': rt, 'message': ''})
                return response
            elif type(rt) is dict:  # return {}
                response.content = rt
                return response
            elif rt is None:  # direct return
                response.content = json.dumps({})
                return response
            else:
                response.content = json.dumps({'message': str(rt)})
                return response

        return decorated

    return paramed_decorator
