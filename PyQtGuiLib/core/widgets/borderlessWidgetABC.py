# -*- coding:utf-8 -*-
# @time:2023/1/1322:36
# @author:LX
# @file:borderlessWidgetABC.py
# @software:PyCharm

from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QWidget,
    QMouseEvent,
    QPoint,
    QPointF,
    QMainWindow,
    QFrame,
    QStackedWidget,
    qt,
    QGraphicsDropShadowEffect,
    QPaintEvent,
    QPainter,
    QBrush,
    QPen,
    QColor,
    QLinearGradient,
    QRect,
    QSize,
    Qt
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

FramelessWindowHint = qt.FramelessWindowHint
ArrowCursor = qt.ArrowCursor
SizeFDiagCursor = qt.SizeFDiagCursor
SizeBDiagCursor = qt.SizeBDiagCursor
SizeHorCursor = qt.SizeHorCursor
SizeVerCursor = qt.SizeVerCursor
LeftButton = qt.LeftButton
OpenHandCursor = qt.OpenHandCursor


# 无边框窗口移动的提示实现类
class Borderless:
    Top = "top"
    Down = "Down"
    Left = "Left"
    Right = "Right"

    # 渐变的方向
    G_Vertical = "vertical"
    G_Horizontal = "horizontal"

    def __init__(self, *args, **kwargs):
        self.scope = 10  # 检测鼠标是否在边缘按下的范围
        self.pressDirection = []  # 记录鼠标点击的边的方向
        self.pressPos = QPoint(0, 0)  # 鼠标按下时的位置
        self.pressState = False  # 按下状态
        self.movePressState = False  # 记录移动时是否时按下的状态

        # 圆角半径,注意这个值不要高于 8 否则四个斜角将失去拉伸功能
        self.r = (7, 7)

        # -------------

        # 背景颜色,边框颜色,边的宽度,画笔风格
        self.w_color = QColor(240, 240, 240, 255)
        self.w_b_color = qt.gray
        self.border_width = 1
        self.open_style = qt.SolidLine

        # 渐变色
        self.is_e_gcolor = False  # 是否启用渐变色
        self.w_g_color = [(0.3, QColor(153, 153, 230, 60)), (1, QColor(98, 98, 147, 255))]
        self.w_g_direction = "vertical"  # 渐变方向

    # 边缘检测
    def isEdge(self, parent: QWidget, pos: QPoint):
        x, y = pos.x(), pos.y()
        w, h = parent.width(), parent.height()

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
    def updateCursor(self, parent: QWidget, pos: QPoint):
        x, y = pos.x(), pos.y()
        w, h = parent.width(), parent.height()
        '''
            先判断四角,再判断四边
        '''
        if (x <= self.scope and x >= 0) and (y >= 0 and y <= self.scope) \
                or (w - x <= self.scope) and (h - y <= self.scope):
            parent.setCursor(SizeFDiagCursor)
        elif (w - x <= self.scope) and (y >= 0 and y <= self.scope) \
                or (x <= self.scope and x >= 0) and (h - y <= self.scope):
            parent.setCursor(SizeBDiagCursor)
        elif (x <= self.scope and x >= 0) or (w - x <= self.scope):
            parent.setCursor(SizeHorCursor)
        elif (y >= 0 and y <= self.scope) or (h - y <= self.scope):
            parent.setCursor(SizeVerCursor)
        else:
            parent.setCursor(ArrowCursor)

        if self.pressDirection:
            return True

    # 扩展边
    def expandEdge(self, parent: QWidget, pos: QPoint):
        if not self.pressState:
            return

        x, y = parent.pos().x(), parent.pos().y()

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
                    parent.resize(parent.width(), distance_)
                    self.pressPos = QPoint(0, distance_)
            if direction == Borderless.Left:
                distance_ = x + pos.x()
                parent.resize(parent.width() - pos.x(), parent.height())
                parent.move(distance_, y)
            if direction == Borderless.Top:
                distance_ = y + pos.y()
                parent.resize(parent.width(), parent.height() - pos.y())
                if Borderless.Left in self.pressDirection:
                    x = x + pos.x()
                parent.move(x, distance_)

    def pressEvent(self, parent: QWidget, e: QMouseEvent) -> None:
        if self.isEdge(parent, e.pos()):
            self.pressState = True
            self.pressPos = e.pos()
        elif e.button() == LeftButton:  # 处理窗口移动
            self.movePressState = True

            if PYQT_VERSIONS in ["PyQt5", "PySide2", "PySide6"]:
                old_pos = e.globalPos()
            if PYQT_VERSIONS == "PyQt6":
                old_pos = e.globalPosition().toPoint()

            self.pressPos = old_pos - parent.pos()

            parent.setCursor(OpenHandCursor)

    def releaseEvent(self) -> None:
        self.pressDirection.clear()
        self.pressPos = QPoint(0, 0)
        self.pressState = False
        self.movePressState = False

    def moveEvent(self, parent: QWidget, e: QMouseEvent) -> None:
        if self.movePressState:
            if PYQT_VERSIONS in ["PyQt5", "PySide2", "PySide6"]:
                old_pos = e.globalPos()
            if PYQT_VERSIONS == "PyQt6":
                old_pos = e.globalPosition().toPoint()
            parent.move(old_pos - self.pressPos)
        self.updateCursor(parent, e.pos())
        self.expandEdge(parent, e.pos())

    def pEvent(self, parent: QWidget, e: QPaintEvent):
        painter = QPainter(parent)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform)  # 抗锯齿

        if self.w_g_direction == Borderless.G_Horizontal:
            gradient = QLinearGradient(0, parent.height(), parent.width(), parent.height())  # 水平线性渐变
        elif self.w_g_direction == Borderless.G_Vertical:
            gradient = QLinearGradient(parent.width(), 0, parent.width(), parent.height())  # 垂直线性渐变
        else:
            gradient = QLinearGradient(0, parent.height(), parent.width(), parent.height())  # 线性渐变

        # 画刷
        bru = QBrush(self.w_color)

        # 画笔
        op = QPen()
        op.setWidth(self.border_width)
        op.setColor(self.w_b_color)
        op.setStyle(self.open_style)

        if self.is_e_gcolor:
            for v, c in self.w_g_color:
                gradient.setColorAt(v, c)
            painter.setBrush(gradient)
        else:
            painter.setBrush(bru)
        painter.setPen(op)

        rect_ = parent.rect()
        rect_.setX(rect_.x() + 2)
        rect_.setY(rect_.y() + 2)
        rect_.setWidth(rect_.width() - 2)
        rect_.setHeight(rect_.height() - 2)

        painter.drawRoundedRect(rect_, self.r[0], self.r[1])

        painter.end()


# 公用方法
class Public:
    # 渐变的方向
    G_Vertical = "vertical"
    G_Horizontal = "horizontal"

    def __init__(self, parent_: QWidget, *args, **kwargs):
        self.parent = parent_
        # 处理父类 公用方法
        self.parent.setAttribute(qt.WA_TranslucentBackground)
        self.parent.setWindowFlags(FramelessWindowHint | qt.Widget)
        self.parent.setMouseTracking(True)  # 开启鼠标跟踪

        # 加上阴影后会出BUG
        # self.geffect = QGraphicsDropShadowEffect(self.parent)
        # self.geffect.setOffset(0, 0)
        # self.geffect.setBlurRadius(10)
        # self.geffect.setColor(QColor(231, 0, 0,250))
        # self.parent.setGraphicsEffect(self.geffect)

        self.borderless = Borderless()

    # 设置圆角半径
    def setRadius(self, r):
        if isinstance(r, int):
            self.borderless.r = (r, r)
        else:
            self.borderless.r = r

    def radius(self) -> tuple:
        return self.borderless.r

    def borderWidth(self) -> int:
        return self.borderless.border_width

    # 设置窗体颜色
    def setWindowColor(self, color: QColor):
        self.borderless.is_e_gcolor = False
        self.borderless.w_color = color

    # 设置边框颜色
    def setWindowBorderColor(self, color: QColor):
        self.borderless.w_b_color = color

    # 设置是否启用渐变色
    def setEnableGColor(self, b: bool, direction="horizontal"):
        self.borderless.is_e_gcolor = b
        self.borderless.w_g_direction = direction

    # 设置窗体渐变色
    def setWindowGColor(self, colos: list, direction="horizontal"):
        self.borderless.is_e_gcolor = True
        self.borderless.w_g_color = colos
        self.borderless.w_g_direction = direction

    # 设置变框风格
    def setBorderStyle(self, style):
        self.borderless.open_style = style

    # 设置边的宽度
    def setBorderWidth(self, w: int):
        self.borderless.border_width = w
