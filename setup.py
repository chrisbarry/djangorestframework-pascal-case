#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path

from setuptools import setup

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

readme = open("README.rst").read()
history = open("HISTORY.rst").read().replace(".. :changelog:", "")
import djangorestframework_pascal_case

def extract_requires():
    with Path('requirements.txt').open() as reqs:
        return [req.strip() for req in reqs if not req.startswith(("#", "--", "-r")) and req.strip()]

setup(
    name="djangorestframework-pascal-case",
    version=djangorestframework_pascal_case.__version__,
    description="PascalCase JSON support for Django REST framework.",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/x-rst",
    author="Avoca",
    author_email="",
    url="https://github.com/avoca/djangorestframework-pascal-case",
    packages=["djangorestframework_pascal_case"],
    package_dir={"djangorestframework_pascal_case": "djangorestframework_pascal_case"},
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=extract_requires(),
    license="BSD",
    zip_safe=False,
    keywords="djangorestframework_pascal_case",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    test_suite="tests",
)
