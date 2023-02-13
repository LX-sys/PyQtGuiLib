# -*- coding:utf-8 -*-
# @time:2023/2/1316:05
# @author:LX
# @file:qtUic.py
# @software:PyCharm
from PyQtGuiLib.header.versions import PYQT_VERSIONS

if PYQT_VERSIONS == "PyQt5":
    from PyQt5 import uic

if PYQT_VERSIONS == "PyQt6":
    from PyQt6 import uic

if PYQT_VERSIONS == "PySide2":
    from PySide2.QtCore import QFile
    from PySide2.QtUiTools import QUiLoader

if PYQT_VERSIONS == "PySide6":
    from PySide6.QtCore import QFile
    from PySide6.QtUiTools import QUiLoader