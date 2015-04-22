#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last modified: Yang Kai (kai.yang@bugua.com)

"""urlpatterns_maker
This urlpatterns_maker is used to auto load url configurations loosely distributed  in the ``views`` package.

Usage:
  1. got views like this
    #################################### my_app/views/default.py #####################################################
    from django_render.annotations import *
    @url(ur'^login/auth$', method=M.POST)
    @post(auth_type=int, auth_id=str, auth_token=str, jpush_registration_id=str)
    def login_auth(request, auth_type, auth_id, auth_token, jpush_registration_id):
        pass
        return True, {'token': login_token, 'user_id': user_id}

    #################################### my_app/views/profile.py #####################################################
    ...

    #################################### my_app/views/friend.py ######################################################
    ...

    #################################### my_app/views/feed.py ########################################################
    ...

  2. config urlpatterns as follow
    #################################### my_app/views/__init__.py ####################################################
    from django_render.url_patterns_maker import urlpatterns_maker
    urlpatterns = urlpatterns_maker(default='^', profile='^my/')

  3. equivalent to
    urlpatterns = patterns('',
                           url(ur'^', include('chooper_api.views.default')),
                           url(ur'^my/', include('chooper_api.views.profile')),
                           url(ur'^friend/', include('chooper_api.views.friend')),
                           url(ur'^feed/', include('chooper_api.views.feed')),
    )

    note that unspecified views(friend.py and feed.py here) got their file name(without extension,
    and surrounded by '^' and '/') as the url regex
"""

import inspect
import os
from django.conf.urls import patterns, include, url

revision = '0.1'


def urlpatterns_maker(**kwargs):
    path_init = inspect.getouterframes(inspect.currentframe())[1][1]
    path_views, file_name_init = os.path.split(path_init)
    path_app, folder_name_views = os.path.split(path_views)
    app_name = os.path.split(path_app)[1]
    files = [f.split('.')[0] for f in os.listdir(path_views) if
             (f.endswith('.py') or os.path.isdir(os.path.join(path_views, f))) and file_name_init != f]
    path_list = path_init.split('/')
    views_index = path_list.index('views')
    prefix = '.'.join(path_list[views_index-1:-1])
    # print(path_init)
    # print(file_name_init)
    # print(path_views)
    # print(path_app)
    # print(folder_name_views)
    # print(app_name)
    # print files
    # print(files)
    urlpatterns = patterns('', )
    for file_name in files:
        if file_name in kwargs:
            urlpatterns += patterns('',
                                    url(ur'{0}'.format(kwargs[file_name]),
                                        include('{0}.{1}'.format(prefix, file_name)))
                                    )
        else:
            urlpatterns += patterns('',
                                    url(ur'^{0}/'.format(file_name),
                                        include('{0}.{1}'.format(prefix, file_name)))
                                    )
        for urlpattern in urlpatterns[-1].url_patterns:
            urlpattern.regex  # url pattern check, thanks to django
    return urlpatterns