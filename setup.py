#!/usr/bin/env python
import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="django-admincommand",
    version="0.1.2",
    description="Execute management commands from the Django admin",
    long_description=read("README.md"),
    author="Anto59290",
    url="https://github.com/BackMarket/django-admincommand",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["django-sneak==0.1"],
    dependency_links=["https://github.com/liberation/django-sneak/tarball/master#egg=django-sneak-0.1"],
)
