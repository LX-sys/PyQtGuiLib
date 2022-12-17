# -*- coding:utf-8 -*-
# @time:2022/12/1711:39
# @author:LX
# @file:borderlessWidget.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QWidget,
    Qt,
    QMouseEvent,
    QPoint
)

'''
    无边框窗口
        可自由拉伸八个方位
'''

class BorderlessWidget(QWidget):
    Top = "top"
    Down = "Down"
    Left = "Left"
    Right = "Right"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800,500)
        self.setObjectName("BorderlessWidget")
        self.setStyleSheet('''
#BorderlessWidget{
background-color:green;
}
''')
        self.setWindowFlags(Qt.FramelessWindowHint)

        # 开启鼠标跟踪
        self.setMouseTracking(True)

        self.scope = 9  # 检测鼠标是否在边缘按下的范围
        self.pressDirection = []  # 记录鼠标点击的边的方向
        self.pressPos = QPoint(0,0) # 鼠标按下时的位置
        self.pressState = False  # 按下状态

    # 边缘检测
    def isEdge(self,pos:QPoint):
        x,y = pos.x(),pos.y()
        w,h = self.width(),self.height()

        if x <= self.scope and x >= 0:
            self.pressDirection.append(BorderlessWidget.Left)
        if w - x <= self.scope:
            self.pressDirection.append(BorderlessWidget.Right)
        if y >= 0 and y <= self.scope:
            self.pressDirection.append(BorderlessWidget.Top)
        if h - y <= self.scope:
            self.pressDirection.append(BorderlessWidget.Down)

        if self.pressDirection:
            return True

    # 更新鼠标的图标
    def updateCursor(self,pos:QPoint):
        x, y = pos.x(), pos.y()
        w, h = self.width(), self.height()

        if (x <= self.scope and x >= 0) or (w - x <= self.scope):
            self.setCursor(Qt.SizeHorCursor)
        elif (y >= 0 and y <= self.scope) or (h - y <= self.scope):
            self.setCursor(Qt.SizeVerCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

        if self.pressDirection:
            return True

    # 扩大边
    def expandEdge(self,pos:QPoint):
        if not self.pressState:
            return

        x,y = self.pos().x(),self.pos().y()
        for direction in self.pressDirection:
            if direction == BorderlessWidget.Right:
                distance = pos - self.pressPos
                distance_ = self.width() + distance.x()
                self.resize(distance_, self.height())
                if BorderlessWidget.Down not in self.pressDirection:
                    self.pressPos = QPoint(distance_, 0)
            if direction == BorderlessWidget.Down:
                distance = pos - self.pressPos
                distance_ = self.height() + distance.y()
                if BorderlessWidget.Right in self.pressDirection:
                    distance_w = self.width() + distance.x()
                    self.resize(distance_w, distance_)
                    self.pressPos = QPoint(distance_w, distance_)
                else:
                    self.resize(self.width(),distance_)
                    self.pressPos = QPoint(0,distance_)
            if direction == BorderlessWidget.Left:
                distance_ = x+pos.x()
                self.resize(self.width()-pos.x(),self.height())
                self.move(distance_, y)
            if direction == BorderlessWidget.Top:
                distance_ = y + pos.y()
                self.resize(self.width(), self.height()-pos.y())
                if BorderlessWidget.Left in self.pressDirection:
                    x = x+pos.x()
                self.move(x,distance_)

    def mousePressEvent(self, e:QMouseEvent) -> None:
        if self.isEdge(e.pos()):
            self.pressState = True
            self.pressPos = e.pos()
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e:QMouseEvent) -> None:
        self.pressDirection.clear()
        self.pressPos = QPoint(0, 0)
        self.pressState = False
        super().mouseReleaseEvent(e)

    def mouseMoveEvent(self, e:QMouseEvent) -> None:
        self.updateCursor(e.pos())
        self.expandEdge(e.pos())

        super().mouseMoveEvent(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = BorderlessWidget()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())