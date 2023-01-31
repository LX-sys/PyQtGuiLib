# -*- coding:utf-8 -*-
# @time:2022/12/2710:59
# @author:LX
# @file:test_gradientBar.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QPushButton,
    qt
)

from PyQtGuiLib.core.widgets import BorderlessWidget
'''
    无边框QWidget窗口 测试
'''

class TestNoBorder(BorderlessWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800,500)

        # self.setEnableGColor(True)
        self.setStyleSheet('''
        WidgetABC{
        qproperty-radius:7;
        qproperty-backgroundColor: rgba(0, 100, 200,255);
        /*qproperty-linearDirection:"LR";
        qproperty-linearColor:"rgba(142, 144, 69, 255) rgba(176, 184, 130, 255) rgba(130, 184, 130, 255)";*/
        qproperty-linear:"LR rgba(142, 144, 69, 255) rgba(176, 184, 130, 255) rgba(130, 184, 130, 255)";
        /*qproperty-border:"2 solid rgba(200, 200, 200, 255)";*/
        }
        #     ''')

        self.flag = False

        self.btn = QPushButton("固定",self)
        self.btn.move(100,100)
        self.btn.clicked.connect(self.test)

    def test(self):
        if self.flag is False:
            self.btn.setText("解放")
            self.windowHandle().setFlags(self.windowFlags() | qt.WindowStaysOnTopHint)
            self.flag= True
        else:
            self.btn.setText("固定")
            self.windowHandle().setFlags(self.windowFlags() | qt.Widget)
            self.flag = False
        self.show()
        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TestNoBorder()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())