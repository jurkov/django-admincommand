#!/usr/bin/env python
import os

from setuptools import find_packages
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), "rb").read().decode("utf8")


setup(
    name="django-admincommand",
    version="0.1.6",
    description="Execute management commands from the Django admin",
    long_description=read("README.md"),
    author="Anto59290",
    url="https://github.com/BackMarket/django-admincommand",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'sneak @ git+https://github.com/rphlo/django-sneak.git',
    ],
)
