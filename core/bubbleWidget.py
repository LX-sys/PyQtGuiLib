# -*- coding:utf-8 -*-
# @time:2022/12/109:49
# @author:LX
# @file:bubbleWidget.py
# @software:PyCharm


from header import (
    sys,
    QApplication,
    QWidget,
    QPainter,
    QPainterPath,
    QPaintEvent,
    QPoint,
    QPolygonF,
    QRectF,
    Qt,
    QPen,
    QFont,
    QColor,
    QLinearGradient,
    re,
    QPushButton,
    QResizeEvent
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

class BubbleWidget(QWidget):
    Top = "top"
    Down = "Down"
    Left = "Left"
    Right = "Right"
    NoNone = "None"
    def __init__(self,*args,**kwargs):
        self.triangle_km = 20  # 三角形的开口大小
        self.w, self.h = 160, 60
        super(BubbleWidget, self).__init__(*args,**kwargs)
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

    def resize(self,w,h) -> None:
        self.w,self.h =w,h
        super(BubbleWidget, self).resize(w,h)

    def setText(self,text:str):
        self.text = text

    def setTextColor(self,color:QColor):
        self.text_color = color

    def setTextSize(self,size:int):
        self.text_size = size

    def setAllText(self,text:int,size=None,color:QColor=None):
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
            ploys = [QPoint(self.triangle_dis, h),
                     QPoint(self.triangle_dis + self.triangle_km, self.box),
                     QPoint(self.triangle_dis+self.triangle_km*2, h)]
        elif self.direction == BubbleWidget.Down:
            h = self.h-self.triangle_h-self.box
            ploys = [QPoint(self.triangle_dis, h+self.box),
                     QPoint(self.triangle_dis+self.triangle_km,h+self.triangle_h),
                     QPoint(self.triangle_dis+self.triangle_km*2, h+self.box)]
        elif self.direction == BubbleWidget.Left:
            ploys = [QPoint(self.box,self.triangle_dis),
                     QPoint(self.triangle_km+self.box,self.triangle_dis-self.triangle_km),
                     QPoint(self.triangle_km+self.box,self.triangle_dis+self.triangle_km)]
        elif self.direction == BubbleWidget.Right:
            ploys = [QPoint(self.w-self.triangle_km,self.triangle_dis-self.triangle_km),
                     QPoint(self.w-self.box,self.triangle_dis),
                     QPoint(self.w-self.triangle_km,self.triangle_dis+self.triangle_km)]
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



class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super(Test, self).__init__(*args,**kwargs)
        self.resize(500,500)

        self.btn = QPushButton("一号玩家",self)
        self.btn.resize(130,100)
        self.btn.move(100,100)

        self.bu = BubbleWidget(self)
        self.bu.resize(160, 80)
        self.bu.setDirection(BubbleWidget.Left)
        self.bu.setTrack(self.btn)
        self.bu.setText("二号是笨蛋")
        # self.bu.move(80,100) # 如果不想手动设置位置可以用下面控件追踪功能



        # # --------
        # self.btn2 = QPushButton("二号玩家",self)
        # self.btn2.resize(130,40)
        # self.btn2.move(400,350)
        #
        # self.bu2 = BubbleWidget(self)
        # self.bu2.setText("你才是哼")
        # # 反向的设置一定要在追踪前面
        # self.bu2.setDirection(BubbleWidget.Down)
        # self.bu2.setTrack(self.btn2)
        # self.bu2.setTextColor(QColor(255, 255, 0))
        # self.bu2.setBColor(QColor(170, 0, 255))
        # self.bu2.setKm(30,10)
        # self.bu2.resize(160,80)
        #
        # self.bu3 = BubbleWidget(self)
        # self.bu3.setText("绿色")
        # self.bu3.setDirection(BubbleWidget.NoNone)
        # self.bu3.setBColor(QColor(170, 255, 127))
        # self.bu3.move(80,300)
        # self.bu3.setKm(80,25)
        # self.bu3.resize(160,80)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()
    sys.exit(app.exec_())