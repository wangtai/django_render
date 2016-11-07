#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from setuptools import setup, find_packages

if sys.version > '3':
    requires = [
        'django >= 1.8.9'
    ]
else:
    requires = [
        'enum34 >= 1.1.2',
        'django >= 1.8.9',
    ]

try:
    long_description = open('README.md').read()
except:
    long_description = ''

setup(
        name='django-render-url',
        version='0.11',
        packages=find_packages(),
        author='WANG Tai',
        author_email='i@wangtai.me',
        url='https://github.com/wangtai/django_render',
        description='a very light django plugin',
        long_description=long_description,
        license='Apache2',
        install_requires=requires,
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
