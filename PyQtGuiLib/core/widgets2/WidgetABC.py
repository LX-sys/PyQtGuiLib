from PyQtGuiLib.core.widgets.borderlessWidgetABC import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    qt,
    Borderless,
    QWidget,
    QMouseEvent,
    QPaintEvent,
    QPainter,
    QLinearGradient,
    QPen,
    QBrush,
    QPoint
)

from PyQtGuiLib.header import CustomStyle

'''
    所有窗口的父类
'''


class WidgetABC(QWidget,CustomStyle):
    # 渐变的方向
    G_Vertical = "vertical"
    G_Horizontal = "horizontal"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(700,500)

        self.setAttribute(qt.WA_TranslucentBackground)
        self.setWindowFlags(qt.FramelessWindowHint | qt.Widget)
        self.setMouseTracking(True)  # 开启鼠标跟踪
        
        # 用于窗口的移动属性
        self.scope = 10  # 检测鼠标是否在边缘按下的范围
        self.pressDirection = []  # 记录鼠标点击的边的方向
        self.pressPos = QPoint(0, 0)  # 鼠标按下时的位置
        self.pressState = False  # 按下状态
        self.movePressState = False  # 记录移动时是否时按下的状态

        # 渐变色
        self.is_e_gcolor = False  # 是否启用渐变色
        self.w_g_direction = "vertical"  # 渐变方向

    # 边缘检测
    def isEdge(self,pos: QPoint):
        x, y = pos.x(), pos.y()
        w, h = self.width(), self.height()

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
    def updateCursor(self, pos: QPoint):
        x, y = pos.x(), pos.y()
        w, h = self.width(), self.height()
        '''
            先判断四角,再判断四边
        '''
        if (x <= self.scope and x >= 0) and (y >= 0 and y <= self.scope) \
                or (w - x <= self.scope) and (h - y <= self.scope):
            self.setCursor(qt.SizeFDiagCursor)
        elif (w - x <= self.scope) and (y >= 0 and y <= self.scope) \
                or (x <= self.scope and x >= 0) and (h - y <= self.scope):
            self.setCursor(qt.SizeBDiagCursor)
        elif (x <= self.scope and x >= 0) or (w - x <= self.scope):
            self.setCursor(qt.SizeHorCursor)
        elif (y >= 0 and y <= self.scope) or (h - y <= self.scope):
            self.setCursor(qt.SizeVerCursor)
        else:
            self.setCursor(qt.ArrowCursor)

        if self.pressDirection:
            return True

    # 扩展边
    def expandEdge(self, pos: QPoint):
        if not self.pressState:
            return

        x, y = self.pos().x(), self.pos().y()

        for direction in self.pressDirection:
            if direction == Borderless.Right:
                if Borderless.Down not in self.pressDirection:
                    distance = pos - self.pressPos
                    distance_ = self.width() + distance.x()
                    self.resize(distance_, self.height())
                    self.pressPos = QPoint(distance_, 0)
            if direction == Borderless.Down:
                distance = pos - self.pressPos
                distance_ = self.height() + distance.y()
                if Borderless.Right in self.pressDirection:
                    distance_w = self.width() + distance.x()
                    self.resize(distance_w, distance_)
                    self.pressPos = QPoint(distance_w, distance_)
                else:
                    self.resize(self.width(), distance_)
                    self.pressPos = QPoint(0, distance_)
            if direction == Borderless.Left:
                distance_ = x + pos.x()
                self.resize(self.width() - pos.x(), self.height())
                self.move(distance_, y)
            if direction == Borderless.Top:
                distance_ = y + pos.y()
                self.resize(self.width(), self.height() - pos.y())
                if Borderless.Left in self.pressDirection:
                    x = x + pos.x()
                self.move(x, distance_)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        if self.isEdge(e.pos()):
            self.pressState = True
            self.pressPos = e.pos()
        elif e.button() == qt.LeftButton:  # 处理窗口移动
            self.movePressState = True

            if PYQT_VERSIONS in ["PyQt5", "PySide2", "PySide6"]:
                old_pos = e.globalPos()
            elif PYQT_VERSIONS == "PyQt6":
                old_pos = e.globalPosition().toPoint()
            else:
                old_pos = QPoint(0,0)

            self.pressPos = old_pos - self.pos()

            self.setCursor(qt.OpenHandCursor)

    def mouseReleaseEvent(self,e:QMouseEvent) -> None:
        self.pressDirection.clear()
        self.pressPos = QPoint(0, 0)
        self.pressState = False
        self.movePressState = False

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        if self.movePressState:
            if PYQT_VERSIONS in ["PyQt5", "PySide2", "PySide6"]:
                old_pos = e.globalPos()
            elif PYQT_VERSIONS == "PyQt6":
                old_pos = e.globalPosition().toPoint()
            else:
                old_pos = QPoint(0, 0)

            self.move(old_pos - self.pressPos)
        self.updateCursor(e.pos())
        self.expandEdge(e.pos())
    
    def paintEvent(self, event:QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform)  # 抗锯齿

        # 绘制边框
        op = QPen()
        op.setWidth(self.get_borderWidth())
        op.setColor(self.get_borderColor())
        # op.setStyle(self.open_style)
        painter.setPen(op)

        # 绘制背景
        if self.is_e_gcolor:
            # 绘制渐变色
            if self.w_g_direction == Borderless.G_Vertical:
                gradient = QLinearGradient(self.width(), 0, self.width(), self.height())  # 垂直线性渐变
            else:
                gradient = QLinearGradient(0, self.height(), self.width(), self.height())  # 水平线性渐变
            for v, c in self.w_g_color:
                gradient.setColorAt(v, c)
            bgcolor = gradient
            painter.setBrush(gradient)
        else:
            # 绘制纯色背景
            bgcolor = QBrush(self.get_backgroundColor())
        painter.setBrush(bgcolor)

        rect_ = self.rect()
        rect_.setX(rect_.x() + self.get_margin())
        rect_.setY(rect_.y() + self.get_margin())
        rect_.setWidth(rect_.width() - self.get_margin())
        rect_.setHeight(rect_.height() - self.get_margin())
        painter.drawRoundedRect(rect_, self.get_radius(), self.get_radius())

        painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = WidgetABC()
    win.setStyleSheet('''
WidgetABC{
qproperty-radius:7;
qproperty-backgroundColor: rgba(165, 138, 255,200);
qproperty-borderWidth:0;
}
    ''')
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())