# -*- coding:utf-8 -*-
# @time:2023/5/1217:39
# @author:LX
# @file:libStyle.py
# @software:PyCharm

from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QWidget,
    QStyle,
    QStyleOption,
    QPainter,
    QStyleHintReturn,
    QStyleOptionButton,
    QFrame
)

class MyStyle(QStyle):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def styleHint(self, stylehint: QStyle.StyleHint, option: QStyleOption, widget: QWidget, returnData: QStyleHintReturn) -> int:
        return 50

    def drawPrimitive(self, pe: QStyle.PrimitiveElement, opt: QStyleOption, p: QPainter, widget: QWidget) -> None:
        super().drawPrimitive(pe,opt,p,widget)


    def drawControl(self, element: QStyle.ControlElement, opt: QStyleOption, p: QPainter, widget: QWidget) -> None:
        if element == QStyle.CE_ShapedFrame:
            print("Dsa")
        # if element == QStyle.CE_ShapedFrame:
        #     super().drawControl(element,opt,p,widget)
        # else:
        #     print("Aaa")
        #     super().drawControl(element,opt,p,widget)

class Test(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(500,300)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(MyStyle())

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
