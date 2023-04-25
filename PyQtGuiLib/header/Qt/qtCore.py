from PyQtGuiLib.header.versions import PYQT_VERSIONS

if PYQT_VERSIONS == "PyQt5":
    from PyQt5.QtCore import *
    from PyQt5.QtCore import pyqtSignal as Signal

if PYQT_VERSIONS == "PyQt6":
    from PyQt6.QtCore import *
    from PyQt6.QtCore import pyqtSignal as Signal

if PYQT_VERSIONS == "PySide2":
    from PySide2.QtCore import *
    from PySide2.QtCore import Property as pyqtProperty

if PYQT_VERSIONS == "PySide6":
    from PySide6.QtCore import *
    from PySide6.QtCore import Property as pyqtProperty
