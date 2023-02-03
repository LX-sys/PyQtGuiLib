'''
    color_HSV
'''
import PySide2

from PyQtGuiLib.header import (
    QApplication,
    sys,
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
    QImage,
    QBrush,
    QVBoxLayout,
    QEvent
)
from PyQt5.QtCore import QObject
from PyQtGuiLib.core.widgets import WidgetABC


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


# 颜色
class ColorHsv(QWidget):
    # 返回颜色rgba
    rgbAChange = Signal(tuple)
    # 返回hsv 中的h (h表示色调)
    hsvChange = Signal(tuple)
    nameChange = Signal(str)

    def __init__(self,*args):
        self._w,self._h = 700,40
        # 移动点的大小
        self._mouse = MousePoint(0,0,4)

        super(ColorHsv, self).__init__(*args)

        self.setFixedHeight(self._h)
        self.setUI()
        self.installEventFilter(self)

    def setUI(self):
        self.pix = QPixmap(self.size())
        self.pix.fill(qt.transparent)
        self.createHuePixmap()
        self.img = QImage(self.pix)

    def paintEvent(self, e: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)
        painter.setPen(qt.white)
        painter.drawPixmap(self.rect(),self.pix)
        painter.drawEllipse(*self._mouse.size(),self._mouse.r()*2,self._mouse.r()*2)

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
        pixel_color = self.img.pixelColor(x, y)
        hsv_v = pixel_color.getHsv()
        color = pixel_color.getRgb()
        cname = pixel_color.name()
        # print("{} - {} - {}".format(hsv_v,color,cname))
        self.hsvChange.emit(hsv_v)
        self.rgbAChange.emit(color)
        self.nameChange.emit(cname)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        self._update(e.pos())

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        self._update(e.pos())

    # 创建HSV颜色条
    def createHuePixmap(self):
        painter = QPainter(self.pix)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform)  # 抗锯齿
        gradient = QLinearGradient(self.width(),0,0, 0)

        i = 0.0
        gradient.setColorAt(0, QColor.fromHsvF(0, 1, 1, 1))
        while i < 1.0:
            gradient.setColorAt(i, QColor.fromHsvF(i,1,1,1))
            i += 1.0/16.0
        gradient.setColorAt(1, QColor.fromHsvF(0, 1, 1, 1))
        painter.setPen(qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRect(self.rect())


class ColorLump(QWidget):
    rgbaChange = Signal(tuple)
    hsvChange = Signal(int)
    nameChange = Signal(str)

    moveed = Signal(int,int,int,int) # 鼠标移动信信号

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # h 色调值  s  v
        self.tonal_value = 350
        self.s_value = 255
        self.v_value = 255
        # 图像位置
        self._pPos_x = 0
        self._pPos_y = 0

        # 移动圆圈的大小
        self._mouse_X = 0
        self._mouse_Y = 0
        self.ellipse_r = 8  # 半径
        self._mouse_color = qt.white  # 圆圈颜色

        # 透明度
        self._alpha = 255

        # 当前颜色值
        self._RGBA = [255, 255, 255, 255]
        # 颜色的十六进制
        self._colorHex = "#ffffff"

        self.pix2 = QPixmap(self.size())
        self.pix2.fill(qt.transparent)

        # --
        self.preview()
        self.createSVPixmap()
        self.updatePreview()

    def paintEvent(self, e: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform)
        # 下面这两句的位置不能换
        painter.drawPixmap(self._pPos_x, self._pPos_y, self.pix2)
        painter.drawPixmap(self._pPos_x, self._pPos_y, self.pix)

        painter.setPen(self._mouse_color)
        painter.drawEllipse(self._mouse_X + self._pPos_x, self._mouse_Y + self._pPos_y,
                            self.ellipse_r * 2, self.ellipse_r * 2)

    def preview(self):
        self.pix = QPixmap(self.size())
        self.pix.fill(qt.transparent)

        painter = QPainter(self.pix)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setCompositionMode(QPainter.CompositionMode_Source)

        gradient = QLinearGradient(0,0,0,360)
        gradient.setColorAt(0,QColor(0,0,0,0))
        gradient.setColorAt(1,QColor(0,0,0,255))

        painter.setPen(qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRect(self.rect())

    def _setSV(self, s: int, v: int) -> None:
        self.s_value = s
        self.v_value = v

        # hsv转成rgba

    def hsvToRgba(self, h: int, s: int, v: int) -> tuple:
        color = QColor()
        color.setHsv(h, s, v)
        # 设置十六进制
        self._colorHex = color.name()
        self._setSV(s, v)
        self._RGBA = list(color.getRgb())
        self._RGBA[3] = self._alpha
        return tuple(self._RGBA)

    def _setMousePos(self, e: QMouseEvent):
        '''
            检查鼠标是否点击在图像上,并设置鼠标位置
        :param e:
        :return:
        '''
        if (e.x() >= -5 + self._pPos_x and
                e.x() <= self._pPos_x + 255 - self.ellipse_r * 2 and
                e.y() >= -5 + self._pPos_y and
                e.y() <= self._pPos_y + 255 - self.ellipse_r * 2
        ):
            self._mouse_X = e.x() - self._pPos_x
            self._mouse_Y = e.y() - self._pPos_y
            self.update()

    def mousePressEvent(self, e: QMouseEvent) -> None:
        self._setMousePos(e)
        # print()
        rgba = self.hsvToRgba(self.tonal_value, e.x(), e.y())
        self._RGBA[0] = rgba[0]
        self._RGBA[1] = rgba[1]
        self._RGBA[2] = rgba[2]
        self._RGBA[3] = rgba[3]
        self.moveed.emit(*rgba)

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        self._setMousePos(e)
        # 这里y需要减一个255,将颜色矫正,不然是反的
        x = e.pos().x() - self._pPos_x
        y = 255 - e.pos().y() + self._pPos_y
        if x >= 0 and x <= 255 and y >= 0 and y <= 255:
            rgba = self.hsvToRgba(self.tonal_value, x, y)
            self._RGBA[0]=rgba[0]
            self._RGBA[1]=rgba[1]
            self._RGBA[2]=rgba[2]
            self._RGBA[3]=rgba[3]
            self.moveed.emit(*rgba)
            self.update()

    def createSVPixmap(self):
        self.pix2 = QPixmap(self.size())
        self.pix2.fill(qt.transparent)

    def updatePreview(self):
        color = QColor()
        color.setHsv(self.tonal_value, 255, 255, self._alpha)

        painter = QPainter(self.pix2)
        painter.setRenderHint(QPainter.Antialiasing)
        gradient = QLinearGradient(0, 0, 360, 0)
        gradient.setColorAt(1, color)
        gradient.setColorAt(0, QColor("#ffffff"))
        painter.setPen(qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRect(self.rect())

class ColorLump2(QWidget):
    rgbaChange = Signal(tuple)
    hsvChange = Signal(int)
    nameChange = Signal(str)

    moveed = Signal(int,int,int,int) # 鼠标移动信信号

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.setUI()


    def setUI(self):
        self.pix = QPixmap(self.size())
        self.pix.fill(qt.transparent)
        self.createPixmap()
        self.img = QImage(self.pix)


    def paintEvent(self, e: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)
        painter.setPen(qt.white)
        painter.drawPixmap(self.rect(),self.pix)
        # painter.drawEllipse(*self._mouse.size(),self._mouse.r()*2,self._mouse.r()*2)

    def createPixmap(self):
        self.pix = QPixmap(self.size())
        self.pix.fill(qt.transparent)

        painter = QPainter(self.pix)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform)

        painter.setCompositionMode(QPainter.CompositionMode_Source)

        gradient = QLinearGradient(0, 0,self.width(),0)
        gradient.setColorAt(0, QColor(255, 255, 255, 255))
        gradient.setColorAt(1, QColor(0, 255, 0, 255))

        painter.setPen(qt.NoPen)
        painter.setBrush(gradient)

        painter.drawRect(self.rect())

# -----------------------------

# 矩形
class ColorRect(WidgetABC):
    # 返回颜色rgba
    rgbAChange = Signal(tuple)
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


    def myEvent(self):
        pass

# 色轮
class ColorWheel(WidgetABC):
    # 返回颜色rgba
    rgbAChange = Signal(tuple)
    # 返回hsv 中的h (h表示色调)
    hsvChange = Signal(int)
    nameChange = Signal(str)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(240,240)
        self.pix = QPixmap(self.size())
        self.pix.fill(qt.transparent)
        self.drawColorWheel()
        self.img = QImage(self.pix)

        self.setMouseTracking(False)
        # self.setRestrictedOperation(False)

    def drawColorWheel(self):
        painter = QPainter(self.pix)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)
        gradient = QConicalGradient(self.width()//2,self.height()//2,6)
        gradient.setColorAt(0,qt.red)
        gradient.setColorAt(60/360,qt.yellow)
        gradient.setColorAt(120/360,qt.green)
        gradient.setColorAt(180/360,QColor(0,253,255))
        gradient.setColorAt(240/360,qt.blue)
        gradient.setColorAt(300/360,QColor(253, 0, 254))
        gradient.setColorAt(1, qt.red)

        bru = QBrush(gradient)
        painter.setPen(qt.NoPen)
        painter.setBrush(bru)
        painter.drawEllipse(self.rect())

        painter.setBrush(QBrush(qt.transparent))
        painter.drawEllipse(20,20,200,200)

    def keyPressEvent(self, event) -> None:
        super().keyPressEvent(event)

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        super().mouseMoveEvent(e)
        if self.pressState:
            x = e.pos().x()
            y = e.pos().y()
            print(self.img.pixelColor(x, y).getRgb())

    def paintEvent(self, e) -> None:
        painter = QPainter(self)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)
        painter.drawPixmap(self.rect(),self.pix)

        painter.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = ColorLump2()
    win.show()

    sys.exit(app.exec_())