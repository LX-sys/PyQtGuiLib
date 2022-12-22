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
    QResizeEvent,
    QPropertyAnimation,
    QPoint,
    QThread,
    QPushButton
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

        self.ani = QPropertyAnimation(self)
        self.ani.setPropertyName(b"pos")
        self.ani.setTargetObject(self)
        self.ani.setDuration(randint(1200,4000))
        self.ani.finished.connect(self.close)

    def setStartValue(self,pos:QPoint):
        self.ani.setStartValue(pos)

    def setEndValue(self,pos:QPoint):
        self.ani.setEndValue(pos)
        self.ani.start()

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

        # 产生气泡
        # self.createBubble()

    # 产生气泡
    def createBubble(self):
        for i in range(randint(1,5)):
            rondomw = randint(5,15)
            sm = SmallBubble(self)
            sm.show()
            sm.w,sm.h= rondomw,rondomw
            sm.move(randint(self.w//2-self.w//4,self.w//2-self.w//10),
                    self.h-randint(20,40))
            sm.setStartValue(sm.pos())
            sm.setEndValue(QPoint(self.w//2-randint(10,40),
                                  self.h//2-randint(10,40)))


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
