# -*- coding:utf-8 -*-
# @time:2022/12/2216:59
# @author:LX
# @file:waterBar.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QWidget,
    Signal,
    Qt,
    QFont,
    QColor,
    QPen,
    QPainter,
    QPaintEvent,
    QFontMetricsF,
    QSize,
    QResizeEvent
)

'''
    水球进度条
'''
from random import randint

# 小气泡
class SmallBubble(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.w,self.h = 15,15

    # 随机产生气泡
    def randomBubble(self,painter:QPainter):
        painter.setPen(QPen(QColor(255,255,255),2))
        painter.drawEllipse(2, 2, self.w, self.h)

    def paintEvent(self, e: QPaintEvent) -> None:
        painter = QPainter()
        painter.begin(self)

        self.randomBubble(painter)
        painter.end()

class WaterBar(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.w,self.h = 200,200
        self.resize(self.w,self.h)

        self.sn = 180
        self.en = 180

        self.water_vat_color = QColor(52, 208, 255) # 水缸里面没有被水覆盖的颜色
        self.water_vat_border_color = QColor(21, 185, 255) # 水缸边的颜色
        self.water_color = QColor(21, 185, 255) # 水的颜色

        # 气泡群
        for i in range(5):
            rondomw = randint(5,15)
            sm = SmallBubble(self)
            sm.w,sm.h= rondomw,rondomw
            sm.move(randint(2,150),randint(100,200))

    def paintEvent(self, e: QPaintEvent) -> None:
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)

        painter.setPen(QPen(self.water_vat_border_color, 2))
        # 画圆
        painter.setBrush(self.water_vat_color)
        painter.drawEllipse(2,2,self.w-4,self.h-4)
        # 画弧
        painter.setBrush(self.water_color)
        painter.drawChord(2,2,self.w-4,self.h-4,self.sn*16,self.en*16)
        painter.end()

    def resize(self, *args) -> None:
        if len(args) == 1 and isinstance(args[0],QSize):
            self.w = args[0].width(),args[0].height()
        else:
            self.w,self.h = args[0],args[1]

        super().resize(self.w,self.h)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = WaterBar()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
