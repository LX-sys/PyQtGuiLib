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

from PyQtGuiLib.core.widgets import StatusBar,TitleBar
from PyQtGuiLib.core.progressBar import GradientBar

'''
    测试 状态栏
'''

class TestStatusBar(BorderlessWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800,500)

        self.setStyleSheet('''
#widget{
background-color:#d4d4d4;
border-radius:30px;
}
        ''')
        # 标题栏
        self.title = TitleBar(self)
        self.title.setTitleText("测试状态栏")
        self.title.setBtnStyle(TitleBar.WinStyle)

        # 状态栏
        self.status = StatusBar(self)
        self.status.setStyleSheet("background-color: rgb(232, 232, 232);")
        self.status.addText("我是标签")
        self.status.addButton("我是按钮")
        self.g = GradientBar()
        self.g.setValue(80)
        self.g.setFixedSize(100,10)
        self.status.addWidget(self.g)
        self.status.addTime(style="color: rgb(0, 0, 127);")

    def resizeEvent(self, event:QResizeEvent) -> None:
        super().resizeEvent(event)
        self.title.updateTitleSize()
        self.status.updateStatusSize()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TestStatusBar()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())