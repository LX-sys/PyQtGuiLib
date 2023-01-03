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
    QPoint,
    QMainWindow,
    QFrame,
    QStackedWidget
)

'''
    无边框窗口
        可自由拉伸八个方位
    
    目前支持的原型窗口
    QMainWindow
    QWidget
    QFrame,
    QStackedWidget
'''


# 无边框窗口移动的提示实现类
class Borderless:
    Top = "top"
    Down = "Down"
    Left = "Left"
    Right = "Right"

    def __init__(self,*args,**kwargs):
        self.scope = 8  # 检测鼠标是否在边缘按下的范围
        self.pressDirection = []  # 记录鼠标点击的边的方向
        self.pressPos = QPoint(0, 0)  # 鼠标按下时的位置
        self.pressState = False  # 按下状态
        self.movePressState = False  # 记录移动时是否时按下的状态

    # 边缘检测
    def isEdge(self,parent:QWidget,pos:QPoint):
        x,y = pos.x(),pos.y()
        w,h = parent.width(),parent.height()

        if x <= self.scope and x >= 0:
            self.pressDirection.append(Borderless.Left)
        if w - x <= self.scope:
            self.pressDirection.append(Borderless.Right)
        if y >= 0 and y <= self.scope:
            self.pressDirection.append(Borderless.Top)
        if h - y <= self.scope:
            self.pressDirection.append(Borderless.Down)

        if self.pressDirection:
            return True

    # 更新鼠标的图标
    def updateCursor(self,parent:QWidget, pos: QPoint):
        x, y = pos.x(), pos.y()
        w, h = parent.width(), parent.height()
        '''
            先判断四角,再判断四边
        '''
        if (x <= self.scope and x >= 0) and (y >= 0 and y <= self.scope) \
                or (w - x <= self.scope) and (h - y <= self.scope):
            parent.setCursor(Qt.SizeFDiagCursor)
        elif (w - x <= self.scope) and (y >= 0 and y <= self.scope) \
                or (x <= self.scope and x >= 0) and (h - y <= self.scope):
            parent.setCursor(Qt.SizeBDiagCursor)
        elif (x <= self.scope and x >= 0) or (w - x <= self.scope):
            parent.setCursor(Qt.SizeHorCursor)
        elif (y >= 0 and y <= self.scope) or (h - y <= self.scope):
            parent.setCursor(Qt.SizeVerCursor)

        else:
            parent.setCursor(Qt.ArrowCursor)

        if self.pressDirection:
            return True

    # 扩展边
    def expandEdge(self,parent:QWidget,pos:QPoint):
        if not self.pressState:
            return

        x,y = parent.pos().x(),parent.pos().y()
        for direction in self.pressDirection:
            if direction == Borderless.Right:
                if Borderless.Down not in self.pressDirection:
                    distance = pos - self.pressPos
                    distance_ = parent.width() + distance.x()
                    parent.resize(distance_, parent.height())
                    self.pressPos = QPoint(distance_, 0)
            if direction == Borderless.Down:
                distance = pos - self.pressPos
                distance_ = parent.height() + distance.y()
                if Borderless.Right in self.pressDirection:
                    distance_w = parent.width() + distance.x()
                    parent.resize(distance_w, distance_)
                    self.pressPos = QPoint(distance_w, distance_)
                else:
                    parent.resize(parent.width(),distance_)
                    self.pressPos = QPoint(0,distance_)
            if direction == Borderless.Left:
                distance_ = x + pos.x()
                parent.resize(parent.width()-pos.x(),parent.height())
                parent.move(distance_, y)
            if direction == Borderless.Top:
                distance_ = y + pos.y()
                parent.resize(parent.width(), parent.height()-pos.y())
                if Borderless.Left in self.pressDirection:
                    x = x+pos.x()
                parent.move(x,distance_)

    def pressEvent(self,parent:QWidget, e:QMouseEvent) -> None:
        if self.isEdge(parent,e.pos()):
            self.pressState = True
            self.pressPos = e.pos()
        elif e.button() == Qt.LeftButton:  # 处理窗口移动
            self.movePressState = True
            self.pressPos = e.globalPos()-parent.pos()
            parent.setCursor(Qt.OpenHandCursor)

    def releaseEvent(self) -> None:
        self.pressDirection.clear()
        self.pressPos = QPoint(0, 0)
        self.pressState = False
        self.movePressState = False

    def moveEvent(self,parent:QWidget, e:QMouseEvent) -> None:
        if self.movePressState:
            parent.move(e.globalPos()-self.pressPos)
        self.updateCursor(parent,e.pos())
        self.expandEdge(parent,e.pos())


# 无边框的主窗口
class BorderlessMainWindow(QMainWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800, 500)

        self.borderless = Borderless()

        self.setWindowFlags(Qt.FramelessWindowHint)
        # 开启鼠标跟踪
        self.setMouseTracking(True)

    def mousePressEvent(self, e:QMouseEvent) -> None:
        self.borderless.pressEvent(self,e)
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e:QMouseEvent) -> None:
        self.borderless.releaseEvent()
        super().mouseReleaseEvent(e)

    def mouseMoveEvent(self, e:QMouseEvent) -> None:
        self.borderless.moveEvent(self,e)
        super().mouseMoveEvent(e)


# 无边框的QWidget
class BorderlessWidget(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800, 500)

        self.borderless = Borderless()

        self.setWindowFlags(Qt.FramelessWindowHint)
        # 开启鼠标跟踪
        self.setMouseTracking(True)

    def mousePressEvent(self, e:QMouseEvent) -> None:
        self.borderless.pressEvent(self,e)
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e:QMouseEvent) -> None:
        self.borderless.releaseEvent()
        super().mouseReleaseEvent(e)

    def mouseMoveEvent(self, e:QMouseEvent) -> None:
        self.borderless.moveEvent(self,e)
        super().mouseMoveEvent(e)


# 无边框的QFrame
class BorderlessFrame(QFrame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800, 500)

        self.borderless = Borderless()

        self.setWindowFlags(Qt.FramelessWindowHint)
        # 开启鼠标跟踪
        self.setMouseTracking(True)

    def mousePressEvent(self, e:QMouseEvent) -> None:
        self.borderless.pressEvent(self,e)
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e:QMouseEvent) -> None:
        self.borderless.releaseEvent()
        super().mouseReleaseEvent(e)

    def mouseMoveEvent(self, e:QMouseEvent) -> None:
        self.borderless.moveEvent(self,e)
        super().mouseMoveEvent(e)


# 无边框的QStackedWidget
class BorderlessStackedWidget(QStackedWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800, 500)

        self.borderless = Borderless()

        self.setWindowFlags(Qt.FramelessWindowHint)
        # 开启鼠标跟踪
        self.setMouseTracking(True)

    def mousePressEvent(self, e:QMouseEvent) -> None:
        self.borderless.pressEvent(self,e)
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e:QMouseEvent) -> None:
        self.borderless.releaseEvent()
        super().mouseReleaseEvent(e)

    def mouseMoveEvent(self, e:QMouseEvent) -> None:
        self.borderless.moveEvent(self,e)
        super().mouseMoveEvent(e)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = BorderlessStackedWidget()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())