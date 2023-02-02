# -*- coding:utf-8 -*-
# @time:2022/12/1711:39
# @author:LX
# @file:borderlessWidget.py
# @software:PyCharm

from PyQtGuiLib.abandonCase.widgets.borderlessWidgetABC import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    Public,
    QWidget,
    QMouseEvent,
    QPaintEvent,
)


# 无边框的QWidget
class BorderlessWidget(QWidget,Public):
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
    win = BorderlessWidget()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())