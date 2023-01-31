# -*- coding:utf-8 -*-
# @time:2023/1/56:11
# @author:LX
# @file:spaceWidget.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QMouseEvent,
    QPainter,
    QPaintEvent,
    QResizeEvent,
    QPoint,
    QRect,
    QPen,
    QBrush,
    QColor,
    QPushButton,
    QScrollArea,
    qt,
    Signal
)

'''
    沙盒 Widget
    SandBoxWidget
'''
class CoreWidget(QWidget):
    pressed = Signal()
    released = Signal()
    mousePosed = Signal(QPoint)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800,600)

        # 记录鼠标是否按下
        self.is_mouse_press = False
        self.start_pos = QPoint(0, 0)  # 按下时的初始位置
        self.move_dis = QPoint(0, 0)  # 移动的距离
        # 网格线之间的间距
        self.grid_line_margin = 30
        self.grid_line_color = QColor(200,200,200)

        self.scanControl()

    # 扫描控件
    def scanControl(self)->list:
        return self.children()

    # 将鼠标的移动操作全部映射到控件上面
    def mouseMapControl(self):
        controls = self.scanControl()

        if not controls:
            return

        for widget in controls:
            old_pos = widget.pos()
            widget.move(old_pos.x()+self.move_dis.x(),old_pos.y()+self.move_dis.y())

    def isPress(self) -> bool:
        return self.is_mouse_press

    def mousePressEvent(self, e: QMouseEvent) -> None:
        self.is_mouse_press = True
        self.start_pos = e.pos()
        self.pressed.emit()
        super().mousePressEvent(e)

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        if self.isPress():
            # self.move_dis = e.globalPos() - self.start_pos
            self.move_dis = e.pos() - self.start_pos
            self.mousePosed.emit(e.pos())
        super().mouseMoveEvent(e)

    def mouseReleaseEvent(self, e:QMouseEvent) -> None:
        self.is_mouse_press = False
        self.start_pos = QPoint(0,0)
        self.released.emit()
        super().mouseReleaseEvent(e)

    # 绘制网格线
    def drawGridLine(self,painter:QPainter):
        op = QPen()
        op.setColor(self.grid_line_color)

        painter.setPen(op)

        h_line_number = self.height()//(self.grid_line_margin-1)
        v_line_number = self.width()//(self.grid_line_margin-1)

        h_n = 0
        for i in range(h_line_number):
            h_rect = (0,h_n,self.width(),h_n)
            painter.drawLine(*h_rect)
            h_n += self.grid_line_margin

        v_n = 0
        for i in range(v_line_number):
            v_rect = (v_n, 0, v_n, self.height())
            painter.drawLine(*v_rect)
            v_n += self.grid_line_margin

    def paintEvent(self, e: QPaintEvent) -> None:
        painter = QPainter(self)

        # 绘制网格线
        self.drawGridLine(painter)

        painter.end()


class SpaceWidget(QScrollArea):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.core = CoreWidget()
        self.setWidget(self.core)

        self.setHorizontalScrollBarPolicy(qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(qt.ScrollBarAlwaysOff)

        self.horizontalScrollBar().setValue(50)

        self.resize(500, 500)
        self.core.resize(self.size())

        self.h =0

        self.core.pressed.connect(lambda :print("Dsa"))
        self.core.mousePosed.connect(self.mopos_event)

        btn = QPushButton("text")
        self.addWidget(btn, QPoint(600, 600))

    # 鼠标位置事件
    def mopos_event(self,v:QPoint):
        print(v)
        mx = v.x()
        my = v.y()
        if mx > self.width():
            self.h += 2
            # if mx > 0:
            #     self.h += 1
            # else:
            #     self.h -= 1
            self.setHorScrollBar(self.h)

    def setHorScrollBar(self,value:int):
        self.horizontalScrollBar().setValue(value)

    def setVorScrollBar(self,value:int):
        self.verticalScrollBar().setValue(value)

    def addWidget(self,widget:QWidget,pos:QPoint):
        widget.setParent(self.core)

        x,y = pos.x(),pos.y()
        core_width = self.core.width()
        core_height = self.core.height()

        if x >= core_width:
            self.core.resize(int(core_width*1.7),core_height)
        elif x > int(core_width*0.7) and x < core_width:
            self.core.resize(int(core_width*1.3),core_height)

        if y >= core_height:
            self.core.resize(self.core.width(),int(core_height*1.7))
        elif y > int(core_height * 0.7) and y < core_height:
            self.core.resize(self.core.width(), int(core_height*1.3))

        widget.move(pos)


    def resizeEvent(self, e: QResizeEvent) -> None:

        super().resizeEvent(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = SpaceWidget()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())