# -*- coding:utf-8 -*-
# @time:2022/12/2710:59
# @author:LX
# @file:test_gradientBar.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QResizeEvent,
    QWidget,
)

from PyQtGuiLib.core.widgets import (
    BorderlessWidget,     # 无边框矩形QWidget窗口
    )

from PyQtGuiLib.core.widgets import StatusBar
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
        # self.title = TitleBar(self)
        # self.title.setTitleText("测试状态栏")
        # self.title.setBtnStyle(TitleBar.WinStyle)

        # 状态栏
        self.status = StatusBar(self)
        self.status.setStatusPos(StatusBar.PosBottom)
        self.status.setStyleSheet("background-color: rgb(232, 100, 232);")
        self.status.addText("我是标签",duration=20)
        self.status.addButton("我是按钮","border:1px solid red;")
        self.g = GradientBar()
        self.g.setValue(80)
        self.g.setFixedSize(100,10)
        self.status.addWidget(self.g)
        self.status.addTime(style="color: rgb(0, 0, 127);")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TestStatusBar()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())