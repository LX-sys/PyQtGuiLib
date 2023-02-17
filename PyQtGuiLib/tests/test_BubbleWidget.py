# -*- coding:utf-8 -*-
# @time:2022/12/1018:13
# @author:LX
# @file:test_BubbleWidget.py
# @software:PyCharm

from PyQtGuiLib.header import PYQT_VERSIONS
from PyQtGuiLib.header import (
    sys,
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout
)

from PyQtGuiLib.core import BubbleWidget

'''
    气泡窗口的测试用例
'''

class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800,500)

        # self.setWindowOpacity(0.5)
        self.vboy = QVBoxLayout(self)

        self.btn = QPushButton("一号玩家",self)
        self.btn.resize(130,60)
        self.btn.move(400,200)

        self.btn2 = QPushButton("二号玩家", self)
        self.btn2.resize(130, 60)
        self.btn2.move(400, 400)

        self.vboy.addWidget(self.btn)
        self.vboy.addWidget(self.btn2)

        # 气泡控件
        self.bu_top = BubbleWidget(self)
        self.bu_top.setDirection(BubbleWidget.Down)
        self.bu_top.setText("hello world")
        self.bu_top.setTrack(self.btn)

        self.bu_top.setStyleSheet('''
BubbleWidget{
qproperty-backgroundColor: rgba(100, 130, 255,200);
qproperty-radius:10;
qproperty-fontSize:15;
qproperty-arrowsSize:12;
qproperty-margin:0;
}
''')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())