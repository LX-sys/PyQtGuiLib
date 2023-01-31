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
    qt,
    QPropertyAnimation,
    QColor,
    QGraphicsBlurEffect,
    QLabel
)

from PyQtGuiLib.core.widgets import BorderlessWidget
'''
    无边框QWidget窗口 测试
'''

class TestNoBorder(BorderlessWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(500,500)

        # self.setEnableGColor(True)
        self.setStyleSheet('''
        WidgetABC{
        qproperty-radius:50;
        qproperty-backgroundColor: rgba(240, 240, 240,255);
        /*qproperty-linearDirection:"LR";
        qproperty-linearColor:"rgba(142, 144, 69, 255) rgba(176, 184, 130, 255) rgba(130, 184, 130, 255)";
        qproperty-linear:"LR rgba(142, 144, 69, 255) rgba(176, 184, 130, 255) rgba(130, 184, 130, 255)";*/
        qproperty-border:"1 solid rgba(0, 0, 0, 255)";
        /*qproperty-ani:xx; 窗口动画*/
        }
        #     ''')



        self.flag = False
        # self.btn = QPushButton("固定", self)
        # self.btn.resize(self.size())
        # self.btn.move(100, 100)
        # self.btn.clicked.connect(self.test)


    def test(self):
        if self.flag is False:
            self.btn.setText("解放")
            self.windowHandle().setFlags(self.windowFlags() | qt.WindowStaysOnTopHint)
            self.flag= True

            self.ani = QPropertyAnimation(self, b"backgroundColor")
            self.ani.setDuration(4000)
            self.ani.setLoopCount(-1)
            self.ani.setStartValue(self.get_backgroundColor())
            self.ani.setKeyValueAt(0.4, QColor(200, 100, 45, 230))
            self.ani.setKeyValueAt(0.6, QColor(200, 50, 45, 200))
            self.ani.setKeyValueAt(0.8, QColor(200, 0, 45, 150))
            self.ani.setEndValue(self.get_backgroundColor())
            #
            self.ani.start()
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