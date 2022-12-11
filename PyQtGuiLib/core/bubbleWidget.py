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
    QSize,
    QFontMetricsF
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
        self.w, self.h = 160, 60  # 默认大小
        super().__init__(*args,**kwargs)
        self.setObjectName("BubbleW")

        self.box = 2  # 边距
        self.triangle_pos = 20  # 三角形在矩形x/y轴的什么位置
        self.triangle_diameter = 20 # 三角形的高度
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
        '''
            widget:需要跟踪的控件
            offset:偏移距离(默认居中)
        '''
        w, h = widget.width(), widget.height()
        x, y = widget.x(), widget.y()
        xw, hy = x + w, h + y
        # 横轴的顶点居中位置
        center_vertex_x = w//2-self.triangle_pos-self.triangle_km+offset
        center_vertex_y = h//2-self.triangle_pos-self.triangle_km+offset
        if self.direction == BubbleWidget.Top:
            self.move(x+center_vertex_x,y+h)
        elif self.direction == BubbleWidget.Down:
            self.move(x+center_vertex_x,y-h)
        elif self.direction == BubbleWidget.Right:
            self.move(x-self.w,y+center_vertex_y)
        elif self.direction == BubbleWidget.Left:
            self.move(xw,y+center_vertex_y)

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

    def setKmPos(self,pos:int):
        self.triangle_pos = pos

    def setKmDiameter(self,diameter:int):
        self.triangle_diameter = diameter

    def setKmM(self,km:int):
        self.triangle_km = km

    def setKm(self,pos:int,diameter:int,km:int):
        '''
            pos:三角形在矩形的距离
            diameter:三角形的高度
            km:三角形开口大小
        '''
        self.setKmPos(pos)
        self.setKmDiameter(diameter)
        self.setKmM(km)

    # 设置方向
    def setDirection(self,d):
        self.direction = d

    def setBColor(self,bcolor:QColor):
        self.bcolor = bcolor

    # 三角形
    def delta(self,ppath:QPainterPath):
        if self.direction == BubbleWidget.Top:
            ploys = [QPointF(self.triangle_pos,self.triangle_diameter+self.box),
                     QPointF(self.triangle_pos+self.triangle_km,self.box),
                     QPointF(self.triangle_pos+self.triangle_km*2,self.triangle_diameter+self.box)]
        elif self.direction == BubbleWidget.Down:
            ploys = [QPointF(self.triangle_pos,self.h-self.triangle_diameter),
                     QPointF(self.triangle_pos+self.triangle_km,self.h-self.box),
                     QPointF(self.triangle_pos+self.triangle_km*2,self.h-self.triangle_diameter)]
        elif self.direction == BubbleWidget.Left:
            ploys = [QPointF(self.triangle_diameter+self.box,self.triangle_pos),
                     QPointF(self.box,self.triangle_pos+self.triangle_km),
                     QPointF(self.triangle_diameter+self.box,self.triangle_pos+self.triangle_km*2)]
        elif self.direction == BubbleWidget.Right:
            ploys=[QPointF(self.w-self.triangle_diameter,self.triangle_pos),
                   QPointF(self.w-self.box,self.triangle_pos+self.triangle_km),
                   QPointF(self.w-self.triangle_diameter,self.triangle_pos+self.triangle_km*2)]
        else:
            return
        ppath.addPolygon(QPolygonF(ploys))

    # 矩形
    def ract_(self,ppath:QPainterPath):
        if self.direction == BubbleWidget.Top:
            rectf = QRectF(self.box, self.box + self.triangle_diameter,
                           self.w - self.box, self.h - self.triangle_diameter - self.box)
        elif self.direction == BubbleWidget.Down:
            rectf = QRectF(self.box, self.box,
                           self.w - self.box, self.h - self.triangle_diameter - self.box)
        elif self.direction == BubbleWidget.Left:
            # self.triangle_diameter+self.box 三角占用的空间
            rectf = QRectF(self.triangle_diameter+self.box,self.box,
                           self.w-self.triangle_diameter,self.h-self.box)
        elif self.direction == BubbleWidget.Right:
            rectf = QRectF(self.box,self.box,
                           self.w-self.triangle_diameter-self.box,
                           self.h-self.box)
        else:
            rectf = QRectF(self.box, self.box,
                           self.w - self.box, self.h - self.box)
        ppath.addRoundedRect(rectf, self.radius,self.radius)

    # 文字
    def text_(self,painter:QPainter):
        f = QFont()
        painter.setFont(f)
        painter.setPen(self.text_color)
        # '''
        #     文字居中位置计算 - 宽
        #     英文:
        #         文字长度*文字大小//3
        #     中文:
        #         文字长度*文字大小*2//3
        # '''
        # n = 1
        # if re.findall(r"[\u4e00-\u9fa5]", self.text):
        #     n = 2

        fs = QFontMetricsF(f)
        fw = int(fs.width(self.text))
        fh = int(fs.height())
        if self.direction == BubbleWidget.Top:
            x = self.w // 2 - fw // 2
            y = self.h // 2+self.triangle_pos
        elif self.direction == BubbleWidget.Down:
            x = self.w // 2 - fw // 2
            y = (self.h-self.triangle_pos//2) // 2
        elif self.direction == BubbleWidget.Left:
            x = (self.w-self.triangle_pos)//2-fw//6
            y = self.h//2+fh//2
        elif self.direction == BubbleWidget.Right:
            x = (self.w-self.triangle_pos)//2-fw//2
            y = self.h//2+fh//2
        else:
            x,y=0,0
            self.text = ""
        painter.drawText(x,y,self.text)

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



