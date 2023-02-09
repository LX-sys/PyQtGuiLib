from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    CustomStyle,
    qt,
    Qt,
    QWidget,
    QMouseEvent,
    QPaintEvent,
    QPainter,
    QLinearGradient,
    QPen,
    QBrush,
    QPoint,
    QColor,
    QEvent
)
import re
import json


'''
    所有窗口的父类
'''

class WidgetABC(QWidget,CustomStyle):
    '''
        支持的自定义样式
    qproperty-radius  --> 圆角  Eg: 7
    qproperty-backgroundColor  --> 背景颜色 Eg: rgba(165, 138, 255,200)
    qproperty-borderWidth --> 边的宽度 Eg: 1
    qproperty-borderStyle --> 边框的风格 Eg: solid
    qproperty-borderColor --> 边框颜色 Eg: rgba(0,100,255,255)
    qproperty-border   --> 边框样式 Eg: "3 solid rgba(0,100,255,255)"
    qproperty-linearDirection; --> 线性渐变的方向 Eg: "LR"
        LR: 左->右
        RL: 右->左
        UD: 上->下
        DU: 下->上
        LRANG: 左上角->右下角
        RLANG: 右下角->左上角
        UDANG: 右上角->左下角
        DUANG: 左下角->右上角
        自定义: [0,0,100,100]或者[0,0,w,h]  这里的 w,h 代只窗口当前的宽和高
    qproperty-linearColor --> 线性渐变色 Eg: "rgba(142, 144, 69, 255) rgba(176, 184, 130, 255) rgba(255, 255, 255, 255)"
    qproperty-linear --> 线性渐变
        Eg: "LR rgba(142, 144, 69, 255) rgba(176, 184, 130, 255) rgba(130, 184, 130, 255)";
        Eg: "[0,0,w,h] rgba(142, 144, 69, 255) rgba(176, 184, 130, 255) rgba(130, 184, 130, 255)";

    '''
    Top = "top"
    Down = "Down"
    Left = "Left"
    Right = "Right"

    # 渐变的方向
    G_Vertical = "vertical"
    G_Horizontal = "horizontal"

    def __init__(self,*args,**kwargs):
        # 窗口操作限制器,当前窗口作为子窗口时,触发
        self.__RestrictedOperation = False if args else True
        if PYQT_VERSIONS in ["PySide6","PySide2"]:
            QWidget.__init__(self,*args, **kwargs)
            CustomStyle.__init__(self,*args, **kwargs)
        else:
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
        self.__is_e_gcolor = False  # 是否启用渐变色
        self.w_g_direction = "horizontal"  # 渐变方向

        # 操作限制
        self.installEventFilter(self)

    # 设置窗口模态
    def setWinModality(self,b:bool):
        self.setWindowModality(Qt.ApplicationModal)

    # 设置 限制操作
    def setRestrictedOperation(self,b:bool):
        self.__RestrictedOperation = b

    # 设置 背景颜色渐变启动
    def setEnableGColor(self,b:bool):
        self.__is_e_gcolor = b

    def isEnableGColor(self)->bool:
        return self.__is_e_gcolor

    # 边缘检测
    def isEdge(self,pos: QPoint):
        x, y = pos.x(), pos.y()
        w, h = self.width(), self.height()

        if x <= self.scope and x >= 0:
            self.pressDirection.append(WidgetABC.Left)
        if w - x <= self.scope:
            self.pressDirection.append(WidgetABC.Right)
        if y >= 0 and y <= self.scope:
            self.pressDirection.append(WidgetABC.Top)
        if h - y <= self.scope:
            self.pressDirection.append(WidgetABC.Down)

        if self.pressDirection:
            return True

    # 更新鼠标的图标
    def updateCursor(self, pos: QPoint):
        x, y = pos.x(), pos.y()
        w, h = self.width(), self.height()
        '''
            先判断四角,再判断四边
        '''
        if self.__RestrictedOperation is False:
            if self.pressDirection:
                return True
            return

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
            if direction == WidgetABC.Right:
                if WidgetABC.Down not in self.pressDirection:
                    distance = pos - self.pressPos
                    distance_ = self.width() + distance.x()
                    self.resize(distance_, self.height())
                    self.pressPos = QPoint(distance_, 0)
            if direction == WidgetABC.Down:
                distance = pos - self.pressPos
                distance_ = self.height() + distance.y()
                if WidgetABC.Right in self.pressDirection:
                    distance_w = self.width() + distance.x()
                    self.resize(distance_w, distance_)
                    self.pressPos = QPoint(distance_w, distance_)
                else:
                    self.resize(self.width(), distance_)
                    self.pressPos = QPoint(0, distance_)
            if direction == WidgetABC.Left:
                distance_ = x + pos.x()
                self.resize(self.width() - pos.x(), self.height())
                self.move(distance_, y)
            if direction == WidgetABC.Top:
                distance_ = y + pos.y()
                self.resize(self.width(), self.height() - pos.y())
                if WidgetABC.Left in self.pressDirection:
                    x = x + pos.x()
                self.move(x, distance_)

    # 绘制背景
    def drawBackgroundColor(self,painter:QPainter):
        # 绘制背景
        if self.__is_e_gcolor:
            # 绘制渐变色
            temp_linearDirection = self.get_linearDirection()
            linearDirection_dict = {
                "w": str(self.width()),
                "h": str(self.height())
            }
            for c in re.findall(r"[a-z]", temp_linearDirection):
                v = linearDirection_dict.get(c, None)
                if v:
                    temp_linearDirection = temp_linearDirection.replace(c, v)

            dir_value = json.loads(temp_linearDirection)
            gradient = QLinearGradient(*dir_value)

            # 分析颜色,并均分
            colors = []
            color_list = re.findall(r"rgba\(.+?\)", self.get_linearColor())
            color_number = len(color_list)
            if color_number > 2:
                paragraph_v = 1 / (color_number - 1)
            else:
                paragraph_v = 0
            v = 0  # 渐变的取值
            for cstr in color_list:
                v_str = re.findall(r"\d{1,3}", cstr)
                colors.append([v, QColor(*[int(i) for i in v_str])])
                if color_number > 2:
                    v += paragraph_v
            # 修改最后一个渐变值
            colors[-1][0] = 1
            for v, c in colors:
                gradient.setColorAt(v, c)
            bgcolor = gradient
            painter.setBrush(gradient)
        else:
            # 绘制纯色背景
            # print("-->",self.get_backgroundColor())
            bgcolor = QBrush(self.get_backgroundColor())

        painter.setBrush(bgcolor)
        # 绘制
        rect_ = self.rect()
        rect_.setX(rect_.x() + self.get_margin())
        rect_.setY(rect_.y() + self.get_margin())
        rect_.setWidth(rect_.width() - self.get_margin())
        rect_.setHeight(rect_.height() - self.get_margin())
        painter.drawRoundedRect(rect_, self.get_radius(), self.get_radius())

    def eventFilter(self, obj: 'QObject', event:QEvent) -> bool:
        # 做为子窗口时,限制事件,event.MouseMove
        if self.__RestrictedOperation is False and event.type() in [event.KeyRelease,event.KeyPress,event.MouseMove]:
            return True
        else:
            return super().eventFilter(obj,event)

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

            # self.setCursor(qt.OpenHandCursor)

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

        # 透明原本边框
        op = QPen()
        op.setColor(qt.transparent)
        painter.setPen(op)

        # 绘制背景
        self.drawBackgroundColor(painter)

        # 绘制边框
        op.setWidth(self.get_borderWidth())
        op.setColor(self.get_borderColor())
        op.setStyle(self.get_borderStyle())
        painter.setPen(op)

        painter.drawRoundedRect(self.rect(),self.get_radius(),self.get_radius())

        painter.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = WidgetABC()
    win.setStyleSheet('''
WidgetABC{
 qproperty-radius:5;
/*qproperty-backgroundColor:rgba(255,0,2,255);*/
/*qproperty-borderColor:rgba(255,0,2,255);*/
}
    ''')
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())