#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: xiLin.ding


from setuptools import setup, find_packages


setup(
    name='django-render-url',
    version='0.9.8.6',
    packages=find_packages(),
    author='WANG Tai',
    author_email='i@wangtai.me',
    url='https://github.com/wangtai/django_render',
    description='a very light django plugin',
    #long_description=open('README.md').read(),
    license='Apache2',
    requires=[
        'Django',
        'enum34'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: System :: Installation/Setup'
    ],
    include_package_data=True,
    zip_safe=False
)
