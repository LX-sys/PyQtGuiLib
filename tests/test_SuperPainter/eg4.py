# -*- coding:utf-8 -*-
# @time:2023/4/717:36
# @author:LX
# @file:eg4.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QColor,
    QPushButton,
    QPoint
)
from PyQtGuiLib.styles import SuperPainter


class Test(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800,600)
        '''
            SuperPainter第四个案例,
            
            在上一个案例,了解了什么是 虚拟对象,这个案例
            将教你如何使用虚拟对象
        '''
        self.painter = SuperPainter()  # 创建一个画师对象,注意这个对象不要创建在paintEvent里面

        # 这个创建一个按钮,等下点击这个按钮来修改图形
        self.btn = QPushButton("修改图形",self)
        self.btn.move(200,50)
        self.btn.clicked.connect(self.updateDraw)

        self.setMouseTracking(True)
        self.cupos = QPoint(-1,-1)

    def mousePressEvent(self, e):
        myrect = self.painter.virtualObj("myrect")
        myrect2 = self.painter.virtualObj("myrect2")
        print("是否点击在myrect图形上",myrect.isClick(self.cupos))
        print("是否点击在myrect2图形上",myrect2.isClick(self.cupos))
        super().mousePressEvent(e)

    def mouseMoveEvent(self, e):
        self.cupos = e.pos()
        myrect2 = self.painter.virtualObj("myrect2")
        if myrect2.isClick(self.cupos):
            myrect2.updateOpenAttr(openAttr={"color": "red", "width": 3})
        else:
            myrect2.updateOpenAttr(openAttr={"color": "green", "width": 3})
        self.update()
        super().mouseMoveEvent(e)

    # 修改图形事件
    def updateDraw(self):
        '''
            所有与虚拟对象有关的方法都在 self.painter.virtualObj() 这个下面

            几乎所有的虚拟对象方法的第一个参数都是 "虚拟对象名称",就像self一样

            这里用的两个方法:
                getVirtualArgs() 获取当前图形的位置大小等信息
                updateArgs() 修改当前图形的位置大小等信息
                updateOpenAttr() 修改当前图形的属性
        '''
        myrect=self.painter.virtualObj("myrect")
        myrect.updateArgs(20,20,100,100)
        myrect.updateOpenAttr(openAttr={"color":"red","width":3})
        myrect.updateBrushAttr(brushAttr={"color":QColor("green")})


        myrect2=self.painter.virtualObj("myrect2")
        myrect2.scale(1.2)
        # myrect2.setHide(True) # True隐藏图形
        # myrect2.move(300,300)
        # myrect2.updateOpenAttr(openAttr={"color":"red","width":3})
        # myrect2.updateBrushAttr(brushAttr={"color":QColor("green")})

        self.update() # 这里必须调用一下,来刷新图形

    def paintEvent(self, QPaintEvent):
        self.painter.begin(self)

        # 创建一个 图形虚拟对象
        self.painter.drawRect(20, 20, 50, 50,openAttr={"color":"green"}, virtualObjectName="myrect")
        self.painter.drawRect(200, 200, 50, 50,openAttr={"color":"green"}, virtualObjectName="myrect2")
        self.painter.drawRoundedRect(10,300,150,80,openAttr={"c":"#00557f"})
        self.painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
