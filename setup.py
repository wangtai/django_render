#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: xilin.ding


from setuptools import setup, find_packages


setup(
    name='django_render',
    version='1.0.1',
    packages=find_packages(),
    author='GaussDing',
    author_email='DDYDLP@gmail.com',
    url='https://github.com/GaussDing',
    description='a very light django plugin',
	long_description=open('README.md').read(),
    license='Apache2',
	requires=[
        'Django'
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
