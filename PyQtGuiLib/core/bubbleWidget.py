# -*- coding:utf-8 -*-
# @time:2022/12/109:49
# @author:LX
# @file:bubbleWidget.py
# @software:PyCharm
from PyQtGuiLib.header import (
    QWidget,
    QPainter,
    QPainterPath,
    QPaintEvent,
    QPolygonF,
    QRectF,
    QFont,
    QColor,
    re,
    QPointF,
    Signal,
    QThread,
    QSize
)

'''
    气泡窗口
    种类一
          /\
    ------  -------
    |             |
    ---------------
    # 后续更新动画
'''

# 弹窗持续时间
class DurationTimeThread(QThread):
    def __init__(self,bub,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.bub = bub  # type:BubbleWidget
        self.dur_time = 3  # 默认秒

    def setDurationTime(self,seconds:int):
        self.dur_time = seconds

    def run(self) -> None:
        if self.dur_time == -1:
            return

        n = 0
        while n != self.dur_time:
            self.sleep(1)
            n+=1
        self.bub.close()


class BubbleWidget(QWidget):
    # 启动/结束事件
    ended = Signal()

    Top = "top"
    Down = "Down"
    Left = "Left"
    Right = "Right"
    NoNone = "None"

    # 弹窗永远存在,不好消失
    Be_Forever = -1

    def __init__(self,*args,**kwargs):
        self.triangle_km = 20  # 三角形的开口大小
        self.w, self.h = 160, 60
        super().__init__(*args,**kwargs)
        self.setObjectName("BubbleW")

        self.box = 2  # 边距
        self.triangle_h = 20  # 三角形高度
        self.triangle_dis = self.w // 2 - self.triangle_km  # 三角形的位置(默认在中心)
        self.direction = BubbleWidget.Top  # 三级形的位置(默认三角形在上面)
        self.radius = 5 # 半径
        self.bcolor = QColor(152, 167, 255)  # 气泡颜色
        self.text = "Bubble"
        self.text_color = QColor(0,85,0)  # 文字颜色
        self.text_size = 15  # 文字大小

        # ==
        self.dtthread = DurationTimeThread(self)
        self.dtthread.start()

    # 弹窗持续时间
    def setDurationTime(self,seconds:int):
        self.dtthread.setDurationTime(seconds)

    # 追踪控件
    def setTrack(self,widget:QWidget,offset:int=0):
        w, h = widget.width() // 2, widget.height()
        x, y = widget.x(), widget.y()
        xw, hy = x + w, h + y
        ww = self.w - self.triangle_dis - self.triangle_km - offset
        if self.direction == BubbleWidget.Top:
            self.move(xw-ww,hy)
        elif self.direction == BubbleWidget.Down:
            self.move(xw - ww, y-self.h-self.triangle_h)
        elif self.direction == BubbleWidget.Right:
            self.move(x-self.w,self.h+self.triangle_dis)
        elif self.direction == BubbleWidget.Left:
            self.move(x+widget.width(),y+widget.height()//2-self.triangle_dis)

    def resize(self,*args) -> None:
        '''
            兼容qt原本的实现
        '''
        if len(args) == 1 and isinstance(args[0],QSize):
            self.w,self.h = args[0].width(),args[0].height()
        else:
            self.w,self.h =args
        super().resize(*args)

    def setText(self,text:str):
        self.text = text

    def setTextColor(self,color:QColor):
        self.text_color = color

    def setTextSize(self,size:int):
        self.text_size = size

    def setAllText(self,text:str,size=None,color:QColor=None):
        self.setText(text)
        if size:
            self.setTextSize(size)
        if color:
            self.setTextColor(color)

    def setKmDis(self,dis:int):
        self.triangle_dis = dis

    def setKmM(self,km:int):
        self.triangle_km = km

    def setKm(self,dis:int,km:int):
        self.setKmDis(dis)
        self.setKmM(km)

    # 设置方向
    def setDirection(self,d):
        self.direction = d
        if self.direction in [BubbleWidget.Top,BubbleWidget.Down]:
            self.triangle_dis = self.w // 2 - self.triangle_km  # 三角形的位置(默认在中心)
        if self.direction in [BubbleWidget.Left,BubbleWidget.Right]:
            self.triangle_dis = self.h // 2   # 三角形的位置(默认在中心)

    def setBColor(self,bcolor:QColor):
        self.bcolor = bcolor

    # 三角形
    def delta(self,ppath:QPainterPath):
        if self.direction == BubbleWidget.Top:
            h = self.triangle_h + self.box
            ploys = [QPointF(self.triangle_dis, h),
                     QPointF(self.triangle_dis + self.triangle_km, self.box),
                     QPointF(self.triangle_dis+self.triangle_km*2, h)]
        elif self.direction == BubbleWidget.Down:
            h = self.h-self.triangle_h-self.box
            ploys = [QPointF(self.triangle_dis, h+self.box),
                     QPointF(self.triangle_dis+self.triangle_km,h+self.triangle_h),
                     QPointF(self.triangle_dis+self.triangle_km*2, h+self.box)]
        elif self.direction == BubbleWidget.Left:
            ploys = [QPointF(self.box,self.triangle_dis),
                     QPointF(self.triangle_km+self.box,self.triangle_dis-self.triangle_km),
                     QPointF(self.triangle_km+self.box,self.triangle_dis+self.triangle_km)]
        elif self.direction == BubbleWidget.Right:
            ploys = [QPointF(self.w-self.triangle_km,self.triangle_dis-self.triangle_km),
                     QPointF(self.w-self.box,self.triangle_dis),
                     QPointF(self.w-self.triangle_km,self.triangle_dis+self.triangle_km)]
        else:
            return
        ppath.addPolygon(QPolygonF(ploys))

    # 矩形
    def ract_(self,ppath:QPainterPath):
        if self.direction == BubbleWidget.Top:
            rectf = QRectF(self.box, self.box + self.triangle_h,
                           self.w - self.box, self.h - self.triangle_h - self.box)
        elif self.direction == BubbleWidget.Down:
            rectf = QRectF(self.box, self.box,
                           self.w - self.box, self.h - self.triangle_h - self.box)
        elif self.direction == BubbleWidget.Left:
            rectf = QRectF(self.triangle_km+self.box,self.box,
                           self.w-self.triangle_km,self.h-self.box)
        elif self.direction == BubbleWidget.Right:
            rectf = QRectF(self.box,self.box,
                           self.w-self.triangle_km-self.box,
                           self.h-self.box)
        else:
            rectf = QRectF(self.box, self.box,
                           self.w - self.box, self.h - self.box)
        ppath.addRoundedRect(rectf, self.radius,self.radius)

    # 文字
    def text_(self,painter:QPainter):
        f = QFont()
        f.setPointSize(self.text_size)
        painter.setFont(f)
        painter.setPen(self.text_color)
        '''
            文字居中位置计算 - 宽
            英文:
                文字长度*文字大小//3
            中文:
                文字长度*文字大小*2//3
        '''
        n = 1
        if re.findall(r"[\u4e00-\u9fa5]", self.text):
            n = 2
        if self.direction == BubbleWidget.Top:
            painter.drawText(self.w // 2 - len(self.text) * self.text_size*n // 3, self.h//2+self.triangle_h, self.text)
        elif self.direction == BubbleWidget.Down:
            painter.drawText(self.w // 2 - len(self.text) * self.text_size * n // 3, self.h//2,
                             self.text)
        else:
            painter.drawText(self.w // 2 - len(self.text) * self.text_size * n // 3, self.h // 2+self.text_size//2,
                             self.text)

    def paintEvent(self, e:QPaintEvent) -> None:
        painter = QPainter()
        painter.begin(self)
        # -------------------
        ppath = QPainterPath()
        # 绘制矩形
        self.ract_(ppath)
        # 绘制三角形
        self.delta(ppath)
        # -------------------
        painter.fillPath(ppath,self.bcolor)
        # 绘制文字
        self.text_(painter)
        painter.end()



