# -*- coding:utf-8 -*-
# @time:2023/2/1316:17
# @author:LX
# @file:test_uic.py
# @software:PyCharm

from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    loadUic
)

app = QApplication(sys.argv)

ui = loadUic(r"xxx.ui")
ui.show()

if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
    sys.exit(app.exec())
else:
    sys.exit(app.exec_())