from PyQtGuiLib.header.versions import PYQT_VERSIONS

if PYQT_VERSIONS == "PyQt5":
    from PyQt5.QtWidgets import *
    from PyQt5.QtWidgets import QDesktopWidget as DesktopWidget

if PYQT_VERSIONS == "PyQt6":
    from PyQt6.QtWidgets import *

if PYQT_VERSIONS == "PySide2":
    from PySide2.QtWidgets import *
    from PySide2.QtWidgets import QDesktopWidget as DesktopWidget

if PYQT_VERSIONS == "PySide6":
    from PySide6.QtWidgets import *