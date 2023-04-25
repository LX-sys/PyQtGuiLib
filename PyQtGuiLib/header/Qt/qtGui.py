from PyQtGuiLib.header.versions import PYQT_VERSIONS

if PYQT_VERSIONS == "PyQt5":
    from PyQt5.QtGui import *

if PYQT_VERSIONS == "PyQt6":
    from PyQt6.QtGui import *
    from PyQt6.QtGui import QGuiApplication as DesktopWidget

if PYQT_VERSIONS == "PySide2":
    from PySide2.QtGui import *
    from PySide2.QtGui import QGuiApplication as DesktopWidget

if PYQT_VERSIONS == "PySide6":
    from PySide6.QtGui import *
    from PySide6.QtGui import QGuiApplication as DesktopWidget