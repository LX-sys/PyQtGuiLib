# -*- coding:utf-8 -*-
# @time:2022/12/2216:59
# @author:LX
# @file:waterBar.py
# @software:PyCharm
from PyQtGuiLib.header import (
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
    qt,
    textSize
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
        self.ani.finished.connect(self.close)

    # 球运行的速度区间
    def setDuration(self,interval:list=[1200,4000]):
        self.ani.setDuration(randint(*interval))

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
    # 进度改变时,发出信号
    valueChange = Signal(int)

    def __init__(self,*args,**kwargs):
        self.ball_interval = [1, 1] # 每次数值改变产生球的数量区间
        self.speed_interval = [1200,4000] # 小球运动的速度区间
        self.size_interval = [5,15] # 小球大小区间

        super().__init__(*args,**kwargs)

        self.w,self.h = 200,200
        self.resize(self.w,self.h)

        self.sn = 180
        self.en = 3.6

        self.water_vat_color = QColor(61, 203, 255,255) # 水缸里面没有被水覆盖的颜色
        self.water_vat_border_color = QColor(21, 185, 255,180) # 水缸边的颜色
        self.water_color = QColor(0, 135, 203) # 水的颜色

        # 当前百分比
        self.cu_value = 0

        # 文字属性
        self.text = "100%"
        self.text_size = 40
        self.text_color = QColor(0, 188, 188)
        self.__is_hide_text = False

    # 产生气泡
    def createBubble(self):
        for i in range(randint(*self.ball_interval)):
            rondomw = randint(*self.size_interval)
            sm = SmallBubble(self)
            sm.setDuration(self.speed_interval)
            sm.show()
            sm.w,sm.h= rondomw,rondomw
            sm.move(randint(self.w//2-self.w//4,self.w//2-self.w//10),
                    self.h-randint(20,40))
            sm.setStartValue(sm.pos())
            sm.setEndValue(QPoint(self.w//2-randint(10,40),
                                  self.h//2-randint(10,40)))

    def setValue(self,v:int):
        self.cu_value = v
        self.text = "{}%".format(v)
        self.update()
        self.valueChange.emit(v)
        self.createBubble()

    def setText(self,text:str):
        self.text = text

    def setTextColor(self,color:QColor):
        self.text_color = color

    def setTextSize(self,size:int):
        self.text_size = size

    def setAllText(self,text:str,color:QColor,size:int):
        self.setText(text)
        self.setTextColor(color)
        self.setTextSize(size)

    def isHideText(self,b:bool):
        self.__is_hide_text = b

    # 设置每个数值变化,球产生的个数区间
    def setBallInterval(self,interval:list):
        self.ball_interval = interval

    # 设置每颗球移动的速度区间
    def setBallSpeedInterval(self,interval:list):
        self.speed_interval = interval

    # 设置每颗球生成的大小区间
    def setBallSizeInterval(self,interval:list):
        self.size_interval = interval

    # 设置水的颜色
    def setWaterColor(self,color:QColor):
        self.water_color = color

    # 设置水缸中没有被水覆盖的颜色
    def setWaterVatColor(self,color:QColor):
        self.water_vat_color = color

    # 设置水缸边缘的颜色
    def setWaterVatBorderColor(self,color:QColor):
        self.water_vat_border_color = color

    # 画水位
    def drawWaterLevel(self,painter:QPainter):
        painter.setPen(QPen(self.water_vat_border_color, 3))
        # 画圆
        painter.setBrush(self.water_vat_color)
        painter.drawEllipse(2,2,self.w-4,self.h-4)

        # --------------
        # painter.drawChord(QtCore.QRect(self.upBlueXPoint, self.upBlueYPoint, self.radius * 2,
        #                                self.radius * 2), (-self.process * 1.8 + 270) * 16,
        #                   self.process * 3.6 * 16)  # blue upper drawChord(x,y, 起始角度，跨越角度）度数要*16.
        # painter.drawChord(QtCore.QRect(self.upBlueXPoint, self.lowBlueYPoint, self.radius * 2,
        #                                self.radius * 2), (-self.process * 1.8 + 270) * 16,
        #                   self.process * 3.6 * 16)  # blue lower

        # 画弧
        painter.setBrush(self.water_color)
        painter.drawChord(2,2,self.w-4,self.h-4,
                          int((-self.cu_value*1.8+270)*16),
                          int(self.cu_value*self.en*16))

    # 绘制文字
    def drawText_(self, painter: QPainter):
        if not self.__is_hide_text:
            # 绘制文字
            f = QFont()
            f.setBold(True)
            f.setPointSize(self.text_size)
            painter.setFont(f)
            painter.setPen(self.text_color)
            # 文字
            fs = textSize(f,self.text)
            fw = fs.width()
            fh = fs.height()
            painter.drawText(self.w // 2 - fw // 2, self.h // 2 + fh // 4, self.text)

    def paintEvent(self, e: QPaintEvent) -> None:
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)

        # 画水位
        self.drawWaterLevel(painter)
        # 画文字
        self.drawText_(painter)

        painter.end()

    def resize(self, *args) -> None:
        if len(args) == 1 and isinstance(args[0],QSize):
            self.w = args[0].width(),args[0].height()
        else:
            self.w,self.h = args[0],args[1]

        super().resize(self.w,self.h)

    def resizeEvent(self, e: QResizeEvent) -> None:
        self.w = e.size().width()
        self.h = e.size().height()
        super().resizeEvent(e)
