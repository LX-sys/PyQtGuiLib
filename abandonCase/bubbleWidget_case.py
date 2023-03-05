from PyQtGuiLib.header import (
    sys,
    QApplication,
    QWidget,
    QHBoxLayout,
    Qt,
    QPainter,
    QPaintEvent,
    QRect,
    QColor,
    QSize,
    QPen,
    QPainterPath
)



'''
    气泡窗口弃案
'''
class BubbleWidget(QWidget):
    def __init__(self,*args,**kwargs):
        super(BubbleWidget, self).__init__(*args,**kwargs)


        self.km = 0 # 默认三角形开口大小是宽度度六分之一
        self.triangle_h = 20 # 三角形高度
        self.w,self.h = 0,0 # 气泡大小
        self.base_edge_color = QColor(232, 232, 232)  # 底边颜色
        self.border_color = QColor(102, 204, 255) # 气泡边框颜色
        self.text = "Bubble"  # 默认文字
        self.resize(200,80)

        self.setObjectName("BubbleW")
        self.setAttribute(Qt.WA_TintedBackground)
        self.setWindowFlags(Qt.WindowShadeButtonHint|Qt.FramelessWindowHint)

        self.hlay = QHBoxLayout(self)
        self.hlay.setContentsMargins(1,1,1,1)
        self.setStyleSheet('''
/*#bubble{
border:1px solid gray;
border-radius:5px;
background-color:rgb(192, 245, 255);
}*/
        ''')

        self.bubble = QWidget()
        self.bubble.setObjectName("bubble")
        self.hlay.addWidget(self.bubble)

    def resize(self, w:int,h:int) -> None:
        self.w,self.h=w,h
        self.km = w//6
        super(BubbleWidget, self).resize(w,h)

    def setBorderColor(self,bcolor:QColor):
        self.border_color = bcolor

    def setText(self,text:str):
        self.text = text

    # 设置开口大小
    def setKm(self,km:int):
        self.km = km

    # 三角形
    def delta(self,painter:QPainter,x:int,km):
        '''

        :param painter: 对象
        :param x: 位置
        :param km: 开口大小
        :return:
        '''
        # 反锯齿渲染
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(self.border_color, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(x,self.triangle_h,x+km,0)
        painter.drawLine(x+km,self.triangle_h,x+km,0)
        painter.setPen(self.base_edge_color)
        painter.drawLine(x+1,self.triangle_h,x+km-1,self.triangle_h)


    def paintEvent(self, e: QPaintEvent) -> None:
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QPen(self.border_color, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawRoundedRect(QRect(1,self.triangle_h,self.w-2,self.h-self.triangle_h-2),5,5)
        painter.drawText(self.w//2-20,self.h//2+15,self.text)
        self.delta(painter,self.w//2,self.km)
        painter.end()
        # super(BubbleWidget, self).paintEvent(e)

class Test(QWidget):
    def __init__(self,*args,**kwargs):
        # super().__init__()
        super(Test, self).__init__(*args,**kwargs)
        self.resize(500,500)

        self.bu = BubbleWidget(self)
        self.bu.setText("蔚蓝色")
        self.bu.setKm(30)  # 气泡开口大小
        self.bu.move(100,50)

        self.bu1 = BubbleWidget(self)
        self.bu1.setKm(60)
        self.bu1.resize(100,80)
        self.bu1.setBorderColor(QColor(89, 90, 255))
        self.bu1.move(100,150)

        self.bu2 = BubbleWidget(self)
        self.bu2.resize(100,100)
        self.bu2.setKm(-40)
        self.bu2.setText("少女粉")
        self.bu2.setBorderColor(QColor(255, 69, 135))
        self.bu2.move(100,250)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()
    sys.exit(app.exec_())