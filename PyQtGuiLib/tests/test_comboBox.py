# -*- coding:utf-8 -*-
# @time:2022/12/296:18
# @author:LX
# @file:test_comboBox.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QMainWindow,
    QThread,
    Signal,
    QColor,
    QThread,
    Qt,
    QPushButton
)

from PyQtGuiLib.core.comboBox import ComboBox

'''
    下拉框 测试用例
'''

class TestComboBox(QMainWindow):
    sed = Signal()
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800,500)

        self.combox = ComboBox(self)
        # self.combox.setFocus()
        self.combox.resize(300,40)
        self.combox.move(100,100)
        print(self.combox.pos())

    def test(self,e):
        print(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TestComboBox()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())