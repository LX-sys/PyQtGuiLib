# -*- coding:utf-8 -*-
# @time:2022/12/1018:31
# @author:LX
# @file:setup.py
# @software:PyCharm

from distutils.core import setup
from setuptools import find_packages


with open("README.md","r") as f:
    des = f.read()


setup(
    name="PyQtGuiLib",
    version="0.0.1.0",
    authors = [
      { name="LX", email="lx984608061@163.com" },
    ],
    description = "Python version of the qt component library.",
    requires-python = ">=3.6",
    readme=des,
    url = "https://github.com/LX-sys/PyQtGuiLib"
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)