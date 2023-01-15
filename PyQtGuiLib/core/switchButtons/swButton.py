from PyQtGuiLib.header import (
    QWidget,
    QBrush,
    QPainter,
    QRect,
    QColor,
    QPaintEvent,
    QMouseEvent,
    qt,
    Signal
)

'''
    开关按钮
'''
class SwitchButton(QWidget):
    clicked = Signal(bool)

    # --- 形状
    Shape_Circle = "circle"
    Shape_Square = "square"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(130,60)

        self.setAttribute(qt.WA_TranslucentBackground)
        self.setWindowFlags(qt.FramelessWindowHint | qt.Widget)

        # 开关标记
        self.is_switch = True

        self.ellipse_x = 1

        self.startTimer(15)
        self.start_color = QColor(0,255,0)
        self.end_color = QColor(255,0,0)
        self.cu_color = self.start_color

        # 背景颜色,球的颜色
        self.bg_color = {"false":QColor(177, 177, 177),"true":QColor(0, 255, 127)}
        self.ball_color = {"false":QColor(234, 234, 234),"true":QColor(0, 255, 127)}

        # 形状
        self.shape = SwitchButton.Shape_Circle

    # 设置形状
    def setShape(self,shape:str):
        self.shape = shape

    # 设置背景颜色
    def setBgColor(self,color_dict:dict):
        '''
            {
                "false":QColor,
                "true":QColor
            }
        '''
        self.bg_color = color_dict

    # 设置运行球的颜色
    def setBallColor(self,color_dict:dict):
        '''
            {
                "false":QColor,
                "true":QColor
            }
        '''
        self.ball_color = color_dict

    # 返回当前的状态
    def state(self) -> bool:
        return not self.is_switch

    # 设置默认状态
    def setDefaultState(self,state:bool):
        if state:
            self.is_switch = not state

    def mousePressEvent(self, e: QMouseEvent) -> None:
        self.is_switch = False if self.is_switch else True
        self.clicked.emit(self.state())
        super().mousePressEvent(e)

    def drawSquareSW(self,painter:QPainter):
        # 画背景颜色
        bg = QBrush(self.bg_color["false"])
        painter.setBrush(bg)
        painter.setPen(qt.NoPen)
        rect_ = QRect(1, 1, self.width() - 3, self.height() - 2)
        painter.drawRoundedRect(rect_, 3, 3)

        # 画球的颜色
        bru = QBrush(self.ball_color["false"])
        painter.setBrush(bru)
        if self.ellipse_x < 0:
            self.ellipse_x = 1
        painter.drawRoundedRect(self.ellipse_x+2, 3, self.height()-3, self.height() - 2-4, 3, 3)
        # painter.drawEllipse(self.ellipse_x, 1, self.height(), self.height() - 2)

        # ----
        if self.is_switch is False:
            bg = QBrush(self.bg_color["true"])
            painter.setBrush(bg)
            painter.drawRoundedRect(rect_, 3, 3)
            # 画球的颜色
            bru = QBrush(self.ball_color["false"])
            painter.setBrush(bru)
            # painter.drawEllipse(self.ellipse_x, 1, self.height(), self.height() - 2)
            painter.drawRoundedRect(self.ellipse_x+2, 3, self.height()-3, self.height() - 2-4, 3, 3)

    # 绘制开关按钮 --
    def drawSwButton(self,painter:QPainter):
        # 画背景颜色
        bg = QBrush(self.bg_color["false"])
        painter.setBrush(bg)
        painter.setPen(qt.NoPen)
        rect_ = QRect(1, 1, self.width() - 3, self.height() - 2)
        painter.drawRoundedRect(rect_, self.height() // 2, self.height() // 2)

        # 画球的颜色
        bru = QBrush(self.ball_color["false"])
        painter.setBrush(bru)
        if self.ellipse_x < 0:
            self.ellipse_x = 1
        painter.drawEllipse(self.ellipse_x, 1, self.height(), self.height() - 2)

        # ----
        if self.is_switch is False:
            bg = QBrush(self.bg_color["true"])
            painter.setBrush(bg)
            painter.drawRoundedRect(rect_, self.height() // 2, self.height() // 2)
            # 画球的颜色
            bru = QBrush(self.ball_color["false"])
            painter.setBrush(bru)
            painter.drawEllipse(self.ellipse_x, 1, self.height(), self.height() - 2)

    def paintEvent(self, e: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)

        # 绘制开关按钮
        if self.shape == SwitchButton.Shape_Square:
            self.drawSquareSW(painter)
        else:
            self.drawSwButton(painter)

        painter.end()

    def timerEvent(self,e) -> None:
        if not self.is_switch and self.ellipse_x < self.width()-self.height()-3:
            self.ellipse_x += (self.width()-self.height()-3)//20
            self.repaint()
        elif self.is_switch and self.ellipse_x >= 2:
            self.ellipse_x -= (self.width()-self.height()-3)//20
            self.repaint()
