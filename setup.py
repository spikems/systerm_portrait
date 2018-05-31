# -*- coding: utf-8 -*-

from setuptools import setup

install_requires = [
    'pymysql',
    'esmre',
    'jieba',
    'elasticsearch'
]


setup(
    name='portrait',
    version='0.1.2',
    description="Please read README.md.",
    install_requires=install_requires,
    zip_safe=False,
    packages=['portrait'],
    package_data={'': ["conf/*.txt"]},
    include_package_data=True,
    platforms='any'
)
