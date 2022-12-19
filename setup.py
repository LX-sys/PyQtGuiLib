# -*- coding:utf-8 -*-
# @time:2022/12/1018:31
# @author:LX
# @file:setup.py
# @software:PyCharm

from distutils.core import setup
from setuptools import find_packages


with open("README.md","r",encoding="utf8") as f:
    des = f.read()


setup(
    name="PyQtGuiLib",
    packages =find_packages(),
    version="0.0.1.6",
    author="LX",
    author_email = "lx984608061@163.com",
    description = "Python version of the qt component library.",
    readme=des,
    url = "https://github.com/LX-sys/PyQtGuiLib",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)