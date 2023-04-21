# -*- coding:utf-8 -*-
# @time:2023/4/2114:44
# @author:LX
# @file:test_drawer.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QPushButton
)

from PyQtGuiLib.core import Drawer,DrawerItem
from PyQtGuiLib.styles import QSSDrak

class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

        self.setStyleSheet(QSSDrak)

        self.drawer = Drawer(self)
        self.drawer.move(10,10)
        self.drawer.resize(300,500)

        for i in range(5):
            btn = QPushButton("hello_{}".format(i))
            ww = QWidget()
            ww.setStyleSheet('''
            background-color: rgb(0, 170, 255);
            ''')
            item = DrawerItem()
            item.setButton(btn)
            item.setWidget(ww)
            self.drawer.addItem(item)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())