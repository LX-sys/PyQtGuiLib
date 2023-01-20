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


        self.btn = QPushButton("一号玩家",self)
        self.btn.resize(130,60)
        self.btn.move(400,200)

        # 气泡控件
        self.bu_top = BubbleWidget(self)
        self.bu_top.setDirection(BubbleWidget.Top)
        self.bu_top.setText("hello world")
        self.bu_top.setTrack(self.btn)

        self.bu_top.setStyleSheet('''
BubbleWidget{
qproperty-backgroundColor: rgba(165, 138, 255,200);
qproperty-radius:10;
qproperty-fontSize:12;
qproperty-arrowsSize:20;
qproperty-margin:3;
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