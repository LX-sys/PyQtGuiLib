# -*- coding:utf-8 -*-
# @time:2023/1/1322:35
# @author:LX
# @file:borderlessMainWindow.py
# @software:PyCharm

from PyQtGuiLib.core.widgets.borderlessWidgetABC import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    Borderless,
    Public,
    QMainWindow,
    QMouseEvent,
    QPaintEvent,
)
from PyQtGuiLib.core.widgets.titleBar import TitleBar
from PyQtGuiLib.core.widgets.statusBar import StatusBar

# 无边框的主窗口
class BorderlessMainWindow(QMainWindow,Public):
    def __init__(self,*args,**kwargs):
        self.child_win = True if args else False
        super().__init__(parent_=self,*args,**kwargs)
        self.resize(800, 500)

        # 默认 创建
        self.createTitleBar()
        self.createStatusBar()

    def createTitleBar(self):
        self.tbar = TitleBar(self)

    def createStatusBar(self):
        self.status = StatusBar(self)

    def titleBar(self)->TitleBar:
        if hasattr(self,"tbar"):
            return self.tbar

    def statusBar(self)->StatusBar:
        if hasattr(self, "status"):
            return self.status

    def mousePressEvent(self, e:QMouseEvent) -> None:
        if not self.child_win:
            self.borderless.pressEvent(self,e)
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e:QMouseEvent) -> None:
        if not self.child_win:
            self.borderless.releaseEvent()
        super().mouseReleaseEvent(e)

    def mouseMoveEvent(self, e:QMouseEvent) -> None:
        if not self.child_win:
            self.borderless.moveEvent(self,e)
        super().mouseMoveEvent(e)

    def paintEvent(self, e: QPaintEvent) -> None:
        self.borderless.pEvent(self,e)
        super().paintEvent(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = BorderlessMainWindow()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())