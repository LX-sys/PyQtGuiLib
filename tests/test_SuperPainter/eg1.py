# -*- coding:utf-8 -*-
# @time:2023/4/717:05
# @author:LX
# @file:eg1.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QColor
)
from PyQtGuiLib.styles import SuperPainter



class Test(QWidget):
    def __init__(self):
        super().__init__()
        '''
            SuperPainter第一个案例, 简单演示使用方法,你会发现和QPainter没什么区别
        '''
        self.painter = SuperPainter() # 创建一个画师对象,注意这个对象不要创建在paintEvent里面

    def paintEvent(self, QPaintEvent):
        self.painter.begin(self)

        # 首先画一个没有任何样式的矩形
        self.painter.drawRect(20,20,50,50)

        # 设置一个画笔,在画两个矩形,这里我们可以看到两个红色边框的画笔
        self.painter.setPen(QColor("red"))
        self.painter.drawRect(100, 20, 50, 50)
        self.painter.drawRect(200, 20, 50, 50)

        # 接下来我们画一个,绿色和蓝色的矩形
        self.painter.setPen(QColor("green"))  # 重新将画笔设置为绿色
        self.painter.drawRect(20, 80, 50, 50)
        self.painter.setPen(QColor("blue"))  # 再次将画笔设置为蓝色
        self.painter.drawRect(100, 80, 50, 50)

        self.painter.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
