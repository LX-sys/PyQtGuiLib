'''
    color_HSV
'''

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
    QBrush
)

from PyQtGuiLib.core.widgets import WidgetABC

# 矩形调色器
class ColorHsv(QWidget):
    # 返回颜色rgba
    rgbAChange = Signal(tuple)
    # 返回hsv 中的h (h表示色调)
    hsvChange = Signal(int)

    def __init__(self,*args):
        self._w = 255
        self._h = 30
        # 移动点的大小
        self._mouse_X = 0
        self._mouse_Y = 0
        self.ellipse_r = 5
        super(ColorHsv, self).__init__(*args)

        self.setFixedSize(self._w, self._h)
        self.setUI()

    def setUI(self):
        self.pix = QPixmap(self._w, self._h)
        self.pix.fill(qt.transparent)
        self.createHuePixmap()
        self.img = QImage(self.pix)

    def paintEvent(self, e: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)
        painter.setPen(qt.white)
        painter.drawPixmap(0,0,self.pix)
        painter.drawEllipse(self._mouse_X,self._mouse_Y,
                            self.ellipse_r*2,self.ellipse_r*2)


    def _update(self,pos:QPoint):
        x,y = pos.x(),pos.y()
        if (x >= 0 and x <= self._w - self.ellipse_r and
            y >= 0 and y <= self._h - self.ellipse_r):
            self._mouse_X = x
            self._mouse_Y = y
            hsv_v = self.img.pixelColor(x, y).getHsv()[0]
            color = self.img.pixelColor(x, y).getRgb()
            self.hsvChange.emit(hsv_v)
            self.rgbAChange.emit(color)
            self.update()

    def mousePressEvent(self, e: QMouseEvent) -> None:
        self._update(e.pos())

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        self._update(e.pos())

    # 创建HSV颜色条
    def createHuePixmap(self):
        painter = QPainter(self.pix)
        i = 0.0
        gradient = QLinearGradient(255,0,0, 0)

        painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        while i< 1.0:
            gradient.setColorAt(i, QColor.fromHsvF(i,1,1,1))
            i +=1.0/16.0
        gradient.setColorAt(1, QColor.fromHsvF(0, 1, 1, 1))
        painter.setPen(qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRect(0, 0, self._w, 255)


# 色轮
class ColorWheel(WidgetABC):
    # 返回颜色rgba
    rgbAChange = Signal(tuple)
    # 返回hsv 中的h (h表示色调)
    hsvChange = Signal(int)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(240,240)
        self.pix = QPixmap(self.size())
        self.pix.fill(qt.transparent)
        self.drawColorWheel()
        self.img = QImage(self.pix)

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

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        super().mouseMoveEvent(e)
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

    win = ColorWheel()
    win.show()

    sys.exit(app.exec_())