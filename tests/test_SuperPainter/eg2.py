# -*- coding:utf-8 -*-
# @time:2023/4/717:20
# @author:LX
# @file:eg2.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QColor,
    Qt,
    qt
)
from PyQtGuiLib.styles import SuperPainter



class Test(QWidget):
    def __init__(self):
        super().__init__()
        '''
            SuperPainter第二个案例,私有属性
            在上一个案例中会发现在画绿色和蓝色的矩形的时候,每次都需要去设置画笔,
            接下来演示 私有属性 来做这件事件
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

        '''
            接下来我们画一个,绿色和蓝色的矩形,使用私有属性,
            只需要通过openAttr来设置
        '''
        self.painter.drawRect(20, 80, 50, 50,openAttr={"color":"green"})
        self.painter.drawRect(100, 80, 50, 50,openAttr={"color":"blue"})
        '''
            看到这里,你会发现,这不就是换了写法吗,
            那么再画一个图形,你会发现这个矩形的边框是红色(上面有设置画笔),并不是blue,
            这就是私有属性的好处,私有有属性不会影响下面其他图形的颜色,
            如果是通过画笔设置的话,是会影响下面画的图形的颜色
        '''
        self.painter.drawRect(200,80,50,50)

        self.painter.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
