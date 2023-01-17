# -*- coding:utf-8 -*-
# @time:2022/12/2710:59
# @author:LX
# @file:test_gradientBar.py
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
    QPushButton,
    qt
)

from PyQtGuiLib.core.widgets import (
    BorderlessMainWindow, # 无边框矩形主窗口
    BorderlessFrame,      # 无边框矩形QFrame窗口
    BorderlessWidget,     # 无边框矩形QWidget窗口
    BorderlessStackedWidget  # 无边框矩形StackedWidget窗口
    )

'''
    继承窗口
'''

class TestNoBorder(BorderlessWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800,500)
        self.setStyleSheet('''
#widget{
background-color:#d4d4d4;
border-radius:30px;
}
        ''')
        # self.setOpacity(0.7)

        self.setEnableGColor(True)
        self.setMask(True)

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