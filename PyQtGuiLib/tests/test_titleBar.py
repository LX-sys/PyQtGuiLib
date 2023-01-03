# -*- coding:utf-8 -*-
# @time:2022/12/2710:59
# @author:LX
# @file:test_gradientBar.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QWidget,
    QResizeEvent
)

from PyQtGuiLib.core.widgets import (
    RoundWidget,   # 圆角QWidget窗口
    BorderlessMainWindow, # 无边框矩形主窗口
    BorderlessFrame,      # 无边框矩形QFrame窗口
    BorderlessWidget,     # 无边框矩形QWidget窗口
    BorderlessStackedWidget  # 无边框矩形StackedWidget窗口
    )

from PyQtGuiLib.core.widgets import TitleBar
'''
    测试 标题栏
'''

class TestTitleBar(BorderlessWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800,500)

        self.setStyleSheet('''
#widget{
background-color:#d4d4d4;
border-radius:30px;
}
        ''')
        self.tbar = TitleBar(self)
        self.tbar.setBtnStyle(TitleBar.WinStyle)
        self.tbar.setStyleSheet("background - color: rgb(232, 232, 232);")

    def resizeEvent(self, event:QResizeEvent) -> None:
        super().resizeEvent(event)
        self.tbar.updateTitleSize()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TestTitleBar()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())