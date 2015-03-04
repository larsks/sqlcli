#!/usr/bin/python

import setuptools

setuptools.setup(
    install_requires=open('requires.txt').readlines(),
    version = 3,
    name = 'sqlcli',
    packages = ['sqlcli'],
    entry_points = {
        'console_scripts': [
            'sqlcli = sqlcli.main:main',
        ],
    }
)

