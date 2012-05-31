#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup


setup_data = {
        'name': 'look-at',
        'version': '1.1',
        'description': "Command line window focus switcher",
        'long_description': open('README.md', 'r').read(),
        'license': 'BSD',
        'packages': [
            'look_at',
            'look_at.scripts',
            ],
        'platforms': "All",
        'classifiers': [
            'Development Status :: 4 - Beta',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2.5',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.2',
            ],
        'entry_points': {
            'console_scripts': [
                'look-at = look_at.scripts.look_at:main',
                ],
            },
        'zip_safe': True,
        'test_suite': "tests.runtests",
        }

setup(**setup_data)
