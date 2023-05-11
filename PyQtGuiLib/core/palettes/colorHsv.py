'''
    color_HSV
'''

from PyQtGuiLib.header import (
    QPixmap,
    QPainter,
    Signal,
    qt,
    QLinearGradient,
    QConicalGradient,
    QColor,
    QMouseEvent,
    QPaintEvent,
    QPoint,
    QWidget,
    QBrush,
    QVBoxLayout,
    QRect,
    QPen
)

# 移动圆圈类
class MousePoint:
    def __init__(self,x=0,y=0,r=0):
        self.__x = x
        self.__y = y
        self.__r = r

    def size(self,x:int=None,y:int=None):
        if x is None or y is None:
            return self.x(), self.y()
        else:
            self.x(x), self.y(y)

    def x(self,v:int=None):
        if v is None:
            return self.__x
        else:
            self.__x = v

    def y(self,v:int=None):
        if v is None:
            return self.__y
        else:
            self.__y = v

    def r(self,v:int=None):
        if v is None:
            return self.__r
        else:
            self.__x = v

    def drawImage(self):
        pass

# 所有调色图像的抽象
class ColorABC(QWidget):
    # 返回颜色rgba
    '''
    rgbaChange:返回(r,g,b,a)
    hsvChange:返回(h,s,v,a)
    nameChange:返回 #xxxxxx
    '''
    rgbaChange = Signal(tuple)
    hsvChange = Signal(tuple)
    nameChange = Signal(str)

    def __init__(self,*args,**kwargs):
        # 移动点的大小
        self._mouse = MousePoint(0, 0, 5)

        super().__init__(*args,**kwargs)

    def setR(self,r):
        self._mouse.r(r)

    def _update(self,pos:QPoint):
        x,y = pos.x(),pos.y()
        if (x >= 0 and x <= self.width() - self._mouse.r() and
            y >= 0 and y <= self.height() - self._mouse.r()):
            self._mouse.size(x,y)
            #
            self.sendSignal(x,y)
            self.update()

    # 发送信号
    def sendSignal(self,x,y):
        color = self.grab(QRect(x, y, 1, 1)).toImage().pixelColor(0, 0)
        # print(color.getRgb())
        self.hsvChange.emit(color.getHsv())
        self.rgbaChange.emit(color.getRgb())
        self.nameChange.emit(color.name())

    # 留给子类重写的部分
    def __painter__(self,painter:QPainter):
        pass

    def mousePressEvent(self, e: QMouseEvent) -> None:
        self._update(e.pos())

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        self._update(e.pos())

    def paintEvent(self, event:QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)

        self.__painter__(painter)
        p = QPen()
        p.setWidth(2)
        painter.setPen(p)
        painter.drawEllipse(*self._mouse.size(), self._mouse.r() * 2, self._mouse.r() * 2)
        painter.end()


class ColorHsv(ColorABC):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.__radius = 5
        self.setFixedHeight(40)
        self.setUI()

    def setRadius(self,r:int):
        self.__radius = r

    def setUI(self):
        self.pix = QPixmap(self.size())
        self.pix.fill(qt.transparent)
        self.createHuePixmap()

    def __painter__(self,painter:QPainter):
        painter.setPen(qt.white)
        painter.drawPixmap(self.rect(),self.pix)

    # 创建HSV颜色条
    def createHuePixmap(self):
        painter = QPainter(self.pix)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform)  # 抗锯齿
        gradient = QLinearGradient(self.width(), 0, 0, 0)

        i = 0.0
        gradient.setColorAt(0, QColor.fromHsvF(0, 1, 1, 1))
        while i < 1.0:
            gradient.setColorAt(i, QColor.fromHsvF(i, 1, 1, 1))
            i += 1.0 / 16.0
        gradient.setColorAt(1, QColor.fromHsvF(0, 1, 1, 1))
        painter.setPen(qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRoundedRect(self.rect(),self.__radius,self.__radius)


class ColorLump(ColorABC):
    def __init__(self,*args,**kwargs):

        super().__init__(*args,**kwargs)
        self.__bgcolor = QColor(0, 255, 0, 255)

        # 鼠标是否过半
        self.is_half = False
        self.setUI()

    def setAlpha(self,a:int):
        self.__bgcolor.setAlpha(a)
        self.colorLayer()

    def setBgColor(self,color:QColor):
        self.__bgcolor = color
        self.colorLayer()

    def bgColor(self) -> QColor:
        return self.__bgcolor

    def setUI(self):
        self.grayLayer()
        self.colorLayer()

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        super().mouseMoveEvent(e)
        # 过半判断
        self.is_half = True if(e.y() > self.height()//2) else False

    # 灰色图层
    def grayLayer(self):
        self.gray_pix = QPixmap(self.size())
        self.gray_pix.fill(qt.transparent)
        self.createGrayPixmap()

    # 彩色图层
    def colorLayer(self):
        self.pix = QPixmap(self.size())
        self.pix.fill(qt.transparent)
        self.createPixmap()

    def __painter__(self,painter:QPainter):
        painter.drawPixmap(self.rect(),self.pix)
        if self.is_half:
            painter.setPen(qt.white)
        painter.drawPixmap(self.rect(), self.gray_pix)

    def createGrayPixmap(self):
        painter = QPainter(self.gray_pix)
        painter.setRenderHints(qt.Antialiasing)

        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(0, 0, 0, 0))
        gradient.setColorAt(1, QColor("#000"))
        painter.setPen(qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRect(self.rect())

    def createPixmap(self):
        painter = QPainter(self.pix)
        painter.setRenderHints(qt.Antialiasing)

        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor("#fff"))

        gradient.setColorAt(1, self.bgColor())

        painter.setPen(qt.NoPen)
        painter.setBrush(gradient)

        painter.drawRect(self.rect())

# -----------------------------

# 矩形
class ColorRect(QWidget):
    # 返回颜色rgba
    rgbaChange = Signal(tuple)
    # 返回hsv 中的h (h表示色调)
    hsvChange = Signal(int)
    nameChange = Signal(str)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(256,256)

        self.setMouseTracking(False)
        self.Init()
        self.myEvent()

    def Init(self):
        self.vlayout = QVBoxLayout(self)
        self.vlayout.setSpacing(1)
        self.vlayout.setContentsMargins(0,0,0,0)

        self.color_hsv = ColorHsv()
        self.color_lump = ColorLump()
        self.vlayout.addWidget(self.color_hsv)
        self.vlayout.addWidget(self.color_lump)

    def setAlpha(self,a:int):
        self.color_lump.setAlpha(a)

    def myEvent(self):
        self.color_hsv.rgbaChange.connect(self.change_lump_event)
        self.color_hsv.hsvChange.connect(self.hsvChange.emit)
        self.color_hsv.nameChange.connect(self.nameChange.emit)
        self.color_lump.rgbaChange.connect(self.rgbaChange.emit)
        self.color_lump.hsvChange.connect(self.hsvChange.emit)
        self.color_lump.nameChange.connect(self.nameChange.emit)

    def change_lump_event(self,rgba:tuple):
        self.rgbaChange.emit(rgba)
        # ----
        self.color_lump.setBgColor(QColor(*rgba))
        self.update()


# 色轮
class ColorWheel(ColorABC):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(240,240)

        # 如果亮度过低,则改变圆圈颜色
        self.is_alpha = False

        self.colors = [(0,QColor(255, 0, 0,255)),
                       (60,QColor(255, 255, 0,255)),
                       (120,QColor(0, 255, 0,255)),
                       (180,QColor(0,255,255,255)),
                       (240,QColor(0, 0, 255,255)),
                       (300,QColor(255, 0, 255,255)),
                       (360,QColor(255, 0, 0,255))
                       ]

        self.setAttribute(qt.WA_TranslucentBackground)
        self.setWindowFlags(qt.FramelessWindowHint | qt.Widget)

        self.setUI()

    def setAlpha(self,a:int):
        for _,color in self.colors:
            color.setAlpha(a)

        self.is_alpha = True if(a <= 220) else False

        self.createColorWheel()

    def setUI(self):
        # 底色
        self.bgColorWheel()
        self.createColorWheel()

    # 色轮底色
    def bgColorWheel(self):
        self.bgpix = QPixmap(self.size())
        self.bgpix.fill(qt.transparent)

        painter = QPainter(self.bgpix)
        painter.setRenderHints(qt.Antialiasing)

        gradient = QConicalGradient(self.width() // 2, self.height() // 2, 6)
        color = QColor(0,0,0,255)
        for v in range(0,420,60):
            gradient.setColorAt(v / 360, color)

        bru = QBrush(gradient)
        painter.setPen(qt.NoPen)
        painter.setBrush(bru)
        painter.drawEllipse(self.rect())

    def createColorWheel(self):
        self.pix = QPixmap(self.size())
        self.pix.fill(qt.transparent)

        painter = QPainter(self.pix)
        gradient = QConicalGradient(self.width() // 2, self.height() // 2, 6)
        painter.setRenderHints(qt.Antialiasing)

        # 绘制
        for v, color in self.colors:
            gradient.setColorAt(v / 360, color)

        bru = QBrush(gradient)
        painter.setPen(qt.NoPen)
        painter.setBrush(bru)
        painter.drawEllipse(self.rect())

        painter.setBrush(QBrush(qt.transparent))
        painter.drawEllipse(20, 20, 200, 255)
        painter.setPen(qt.white)


    def __painter__(self,painter:QPainter):
        painter.drawPixmap(self.rect(), self.bgpix)
        if self.is_alpha:
            painter.setPen(qt.white)
        painter.drawPixmap(self.rect(), self.pix)