# -*- coding:utf-8 -*-
# @time:2023/1/1322:39
# @author:LX
# @file:borderlessFrame.py
# @software:PyCharm

from PyQtGuiLib.core.widgets.borderlessWidgetABC import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    Borderless,
    Public,
    QFrame,
    QMouseEvent,
    QPaintEvent,
)

# 无边框的QFrame
class BorderlessFrame(QFrame,Public):
    def __init__(self,*args,**kwargs):
        self.child_win = True if args else False
        super().__init__(parent_=self,*args,**kwargs)
        self.resize(800, 500)

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
    win = BorderlessFrame()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())