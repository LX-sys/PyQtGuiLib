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

class TPushButton(QPushButton):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setWindowFlags(Qt.WindowStaysOnTopHint| Qt.WindowTransparentForInput)


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


        self.btn1 = QPushButton("test2",self)
        self.btn = TPushButton("test", self)
        self.btn.move(200,0)
        self.btn.clicked.connect(lambda :print("111"))

        self.btn1.clicked.connect(self.test)

    def test(self,e):
        print(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TestComboBox()

    c = Signal(int)

    # print(c.signatures)
    # c.__get__(win,object())
    setattr(TestComboBox,"ked",c)
    print(TestComboBox.__dict__)
    # TestComboBox.ked.signatures = TestComboBox.property(lambda win: object(), lambda win, v: None, lambda win: None)
    # print(TestComboBox.sed.signatures)
    # print(TestComboBox.ked.signatures)
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())