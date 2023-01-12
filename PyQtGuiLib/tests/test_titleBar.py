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
    QColor,
    QResizeEvent
)

from PyQtGuiLib.core.widgets import (
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
        # self.setEnableGColor(True)

        self.tbar = TitleBar(self)
        self.tbar.setTitlePos(TitleBar.Title_Center)
        self.tbar.setTitleText("测试标题栏")
        self.tbar.setTitleColor(QColor(0,0,0,255))
        # self.tbar.setTitleIcon(r"/Applications/Python 3.8/save/PyQtGuiLib/PyQtGuiLib/tests/image/1.png")
        self.tbar.setBtnStyle(TitleBar.MacStyle)
        self.tbar.setStyleSheet("background-color: transparent;")

    def resizeEvent(self, event:QResizeEvent) -> None:
        super().resizeEvent(event)
        self.tbar.updateTitleSize()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TestTitleBar()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())