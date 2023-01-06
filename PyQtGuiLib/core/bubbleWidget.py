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
    QPointF,
    Signal,
    QThread,
    QSize,
    QFontMetricsF,
    textSize
)

from PyQtGuiLib.animation.lmlmAni import LmLmAnimation
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
    finished = Signal()  # 完成信号
    def __init__(self,bub,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.bub = bub  # type:BubbleWidget
        self.dur_time = 3  # 默认秒

    def setDurationTime(self,seconds:int):
        self.dur_time = seconds

    def run(self) -> None:
        if self.dur_time == -1:
            self.finished.emit()
            return

        n = 0
        while n != self.dur_time:
            self.sleep(1)
            n+=1
        self.finished.emit()


class BubbleWidget(QWidget):
    # 启动/结束事件
    finished = Signal()

    Top = "top"
    Down = "Down"
    Left = "Left"
    Right = "Right"
    NoNone = "None"

    # 弹窗永远存在,不好消失
    Be_Forever = -1

    def __init__(self,*args,**kwargs):
        self.triangle_km = 10  # 三角形的开口大小
        self.w, self.h = 160, 70  # 默认大小
        super().__init__(*args,**kwargs)
        self.resize(self.w,self.h)
        self.setObjectName("BubbleW")

        self.box = 2  # 边距
        self.triangle_pos = 20  # 三角形在矩形x/y轴的什么位置
        self.triangle_diameter = 15 # 三角形的高度
        self.direction = BubbleWidget.Top  # 三级形的方向(默认三角形在上面)
        self.radius = 5 # 半径
        self.bcolor = QColor(152, 167, 255)  # 气泡颜色
        self.text = "Bubble"  # 文本
        self.text_color = QColor(0,85,0)  # 文字颜色
        self.text_size = 16  # 文字大小
        self.is_aim = False # 判断是否需要动画(动画的优先级姚高于持续时间 先执行动画->在执行气泡持续时间)
        self.is_durtime = False # 是否开启气泡窗口的持续时间
        # ===
        self.dtthread = DurationTimeThread(self)  # 气泡持续时间线程
        self.lmlm = LmLmAnimation()  # 动画
        self.lmlm.setTargetObject(self) # 设置动画的目标
        #
        self.dtthread.finished.connect(self.finish_event)

    # 气泡启动动画
    def setAnimationEnabled(self,b:bool,duration_time:int=2000):
        if b:
            self.is_aim = True
            self.lmlm.setDuration(duration_time)
            self.lmlm.start()
            if self.is_durtime:
                def _(self):
                    self.dtthread.start()
                    self.lmlm.disconnect()  # 这里必须断开链接,
                self.lmlm.finished.connect(lambda :_(self))

        else:
            self.is_aim = False

    # 气泡持续时间
    def setDurationTime(self, seconds: int):
        if seconds != BubbleWidget.Be_Forever:
            self.is_durtime = True
            self.dtthread.setDurationTime(seconds)
            if self.is_aim is False:
                self.dtthread.start()
        else:
            self.is_durtime = False

    # 完成事件
    def finish_event(self):
        if self.is_durtime and self.is_aim is False:
            self.close()
        else:
            self.lmlm.setMode(self.lmlm.Hide)
            self.lmlm.start()
            # self.lmlm.finished.connect(self.finished.emit())

    # 追踪控件
    def setTrack(self,widget:QWidget,offset:int=0):
        '''
            widget:需要跟踪的控件
            offset:偏移距离(默认居中)
        '''
        w, h = widget.width(), widget.height()
        x, y = widget.x(), widget.y()
        xw, hy = x + w, h + y
        # 轴上的顶点居中位置
        center_vertex_x = w//2-self.triangle_pos-self.triangle_km+offset
        center_vertex_y = h//2-self.triangle_pos-self.triangle_km+offset
        if self.direction == BubbleWidget.Top:
            self.move(x+center_vertex_x,y+h)
        elif self.direction == BubbleWidget.Down:
            self.move(x+center_vertex_x,y-self.h)
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
                     QPointF(self.triangle_pos+self.triangle_km<<1,self.triangle_diameter+self.box)]
        elif self.direction == BubbleWidget.Down:
            ploys = [QPointF(self.triangle_pos,self.h-self.triangle_diameter),
                     QPointF(self.triangle_pos+self.triangle_km,self.h-self.box),
                     QPointF(self.triangle_pos+self.triangle_km<<1,self.h-self.triangle_diameter)]
        elif self.direction == BubbleWidget.Left:
            ploys = [QPointF(self.triangle_diameter+self.box,self.triangle_pos),
                     QPointF(self.box,self.triangle_pos+self.triangle_km),
                     QPointF(self.triangle_diameter+self.box,self.triangle_pos+self.triangle_km<<1)]
        elif self.direction == BubbleWidget.Right:
            ploys =[QPointF(self.w-self.triangle_diameter,self.triangle_pos),
                   QPointF(self.w-self.box,self.triangle_pos+self.triangle_km),
                   QPointF(self.w-self.triangle_diameter,self.triangle_pos+self.triangle_km<<1)]
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
        f.setPointSize(self.text_size)
        painter.setFont(f)
        painter.setPen(self.text_color)
        # 文字大小
        fs = textSize(f,self.text)
        fw = fs.width()
        fh = fs.height()

        if self.direction == BubbleWidget.Top:
            x = (self.w - fw) // 2
            y = self.h // 2+self.triangle_diameter
        elif self.direction == BubbleWidget.Down:
            x = (self.w - fw) // 2
            y = (self.h-self.triangle_diameter+fh) // 2
        elif self.direction == BubbleWidget.Left:
            x = (self.w-self.triangle_diameter-fw//2)//2
            y = (self.h + fh)//2
        elif self.direction == BubbleWidget.Right:
            x = (self.w-self.triangle_diameter)//2-fw//2
            y = (self.h + fh) // 2
        else:
            x,y = 0,0
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



