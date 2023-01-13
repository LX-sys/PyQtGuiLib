# -*- coding:utf-8 -*-
# @time:2023/1/1214:50
# @author:LX
# @file:test_rollWidget.py
# @software:PyCharm

from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QPushButton
)

'''
    滚动栏 测试用例
'''

from PyQtGuiLib.core import RollWidget
from PyQtGuiLib.styles import ButtonStyle


class Test_RollWidget(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800,600)

        # 滚动栏
        self.rlw = RollWidget(self)
        self.rlw.resize(500,60)
        self.rlw.move(10,100)
        self.rlw.changed.connect(self.test)

        self.addbtn = QPushButton("动态添加",self)
        self.addbtn.move(10,10)
        self.addbtn.clicked.connect(self.AddBtn)

        # ---
        for i in range(3):
            btn = QPushButton("test_{}".format(i))
            btn.setStyleSheet("background-color:rgb(255, 255, 127);")
            self.rlw.addWidget(btn)

    def test(self,wid):
        print(wid.text())

    def AddBtn(self):
        bt = QPushButton("dsa")
        bt.setStyleSheet(ButtonStyle.contrastStyle())
        self.rlw.addWidget(bt)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test_RollWidget()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())