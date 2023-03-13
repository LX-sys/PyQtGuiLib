# -*- coding:utf-8 -*-
# @time:2023/3/1311:27
# @author:LX
# @file:test_toolList.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    qt,
    QPushButton,
    QHBoxLayout,
    QListWidget

)
'''
    ToolListWidget 测试
'''

from functools import partial

from PyQtGuiLib.core import ToolListWidget,ToolListItem


class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.resize(600,600)

        self.hboy = QHBoxLayout(self)

        self.left = ToolListWidget()
        self.left.setFixedWidth(200)
        self.rigth = QWidget()
        self.rigth.setStyleSheet('''
        border:1px solid red;
        ''')

        self.hboy.addWidget(self.left)
        self.hboy.addWidget(self.rigth)

        # temp1 = ToolListItem("测试数据一号")
        # temp2 = ToolListItem("测试数据二号")
        #
        # self.left.addItem(temp1)
        # self.left.addItem(temp2)
        self.left.addItems(["111","xx"])
        print(self.left.getUnfoldItems())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())