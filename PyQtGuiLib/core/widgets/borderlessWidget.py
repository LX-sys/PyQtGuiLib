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
        self.pressDirection = None  # 记录鼠标点击的边的方向
        self.pressPos = QPoint(0,0) # 鼠标按下时的位置
        self.pressState = False  # 按下状态

    # 边缘检测
    def isEdge(self,pos:QPoint):
        x,y = pos.x(),pos.y()
        w,h = self.width(),self.height()

        if x <= self.scope and x >= 0:
            self.pressDirection = BorderlessWidget.Left
        elif w - x <= self.scope:
            self.pressDirection = BorderlessWidget.Right
        elif y >= 0 and y <= self.scope:
            self.pressDirection = BorderlessWidget.Top
        elif h - y <= self.scope:
            self.pressDirection = BorderlessWidget.Down
        else:
            self.pressDirection = None

        if self.pressDirection:
            return True

    # 更新鼠标的图标
    def updateCursor(self,pos:QPoint):
        x, y = pos.x(), pos.y()
        w, h = self.width(), self.height()

        if x <= self.scope and x >= 0:
            self.setCursor(Qt.SizeHorCursor)
        elif w - x <= self.scope:
            self.setCursor(Qt.SizeHorCursor)
        elif y >= 0 and y <= self.scope:
            self.setCursor(Qt.SizeVerCursor)
        elif h - y <= self.scope:
            self.setCursor(Qt.SizeVerCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

        if self.pressDirection:
            return True

    # 扩大边
    def expandEdge(self,pos:QPoint):
        if not self.pressState:
            return
        print(pos,self.pressPos)

        x,y = self.pos().x(),self.pos().y()

        if self.pressDirection == BorderlessWidget.Right:
            distance = pos - self.pressPos
            distance_ = self.width() + distance.x()
            self.resize(distance_, self.height())
            self.pressPos = QPoint(distance_, 0)
        elif self.pressDirection == BorderlessWidget.Down:
            distance = pos - self.pressPos
            distance_ = self.height() + distance.y()
            self.resize(self.width(),distance_)
            self.pressPos = QPoint(0,distance_)
        elif self.pressDirection == BorderlessWidget.Left:
            pass
        elif self.pressDirection == BorderlessWidget.Top:
            pass

    def mousePressEvent(self, e:QMouseEvent) -> None:
        if self.isEdge(e.pos()):
            self.pressState = True
            self.pressPos = e.pos()
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e:QMouseEvent) -> None:
        self.pressDirection = None
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