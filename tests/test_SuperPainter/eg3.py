# -*- coding:utf-8 -*-
# @time:2023/4/717:30
# @author:LX
# @file:eg3.py
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
            SuperPainter第三个案例,
            这里 将一个全新的概念 虚拟对象,
            
            那为什么需要 虚拟对象 呢?
            原本通过QPainter绘制的图形,当你想要动态修改的时候会发现很困难,无从下手,
            那如果图形是一个对象呢,对象是具有属性的,当我想要修改图形时,只需要修改对应图形的属性就好.
            这就是 虚拟对象 存在的意义
        '''
        self.painter = SuperPainter() # 创建一个画师对象,注意这个对象不要创建在paintEvent里面

    def paintEvent(self, QPaintEvent):
        self.painter.begin(self)

        '''
            将一个图形变成虚拟对象的方法很简单,需要用到一个关键字参数
            virtualObjectName,给这个参数给一个虚拟对象名称就完成了,
            同时这句绘图代码,也可以称为 图形虚拟对象的初始化
        '''
        self.painter.drawRect(20,20,50,50,virtualObjectName="myrect")

        self.painter.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
