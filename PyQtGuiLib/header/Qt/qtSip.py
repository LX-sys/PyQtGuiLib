# -*- coding:utf-8 -*-
# @time:2023/1/3013:03
# @author:LX
# @file:qtSip.py
# @software:PyCharm
from PyQtGuiLib.header.versions import PYQT_VERSIONS

if PYQT_VERSIONS == "PyQt5":
    from PyQt5.sip import delete


if PYQT_VERSIONS == "PyQt6":
    from PyQt6.sip import delete

if PYQT_VERSIONS == "PySide2":
    try:
        from PySide2.sip import delete
    except:
        pass

if PYQT_VERSIONS == "PySide6":
    try:
        from PySide6.sip import delete
    except:
        pass