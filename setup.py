# -*- coding:utf-8 -*-
# @time:2022/12/1018:31
# @author:LX
# @file:setup.py
# @software:PyCharm

from distutils.core import setup
from setuptools import find_packages


setup(
    name="PyQtGuiLib",
    packages =find_packages(),
    version="1.2.17.7",
    author="LX",
    author_email = "lx984608061@163.com",
    description = "Python version of the qt component library.",
    long_description=open('README.md', 'r',encoding="utf8").read(),
    long_description_content_type="text/markdown",
    url = "https://github.com/LX-sys/PyQtGuiLib",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)