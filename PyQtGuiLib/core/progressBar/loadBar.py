# -*- coding:utf-8 -*-
# @time:2022/12/2214:52
# @author:LX
# @file:loadBar.py
# @software:PyCharm
from PyQtGuiLib.header import (
    QWidget,
    Signal,
    QFont,
    QColor,
    QPen,
    QPainter,
    QPaintEvent,
    QSize,
    QResizeEvent,
    qt,
    textSize,
    pyqtProperty
)
from PyQtGuiLib.core.widgets import WidgetABC

'''
    加载进度条
'''
class LoadBar(WidgetABC):
    # 进度改变时,发出信号
    valueChange = Signal(int)

    def __init__(self,*args,**kwargs):
        self.w,self.h =30, 50

        self.edge_distance_x = 5  # 水平方向的边距
        self._outer_radius, self._inner_radius = 20, 15  # 内外圆角

        # 每一段大小
        self.degree = (self.w - self.edge_distance_x * 4) / 100
        # 当前值
        self.cu_value = 0
        self.max_value = 100

        super().__init__(*args,**kwargs)

        # 外框和进度条的颜色
        self.outline_border_color = QColor(0,0,0)
        self.bar_color = QColor(0,82,70)

        # 文字属性
        self.text = "100%"
        self.__is_hide_text = False  # 是否隐藏文字选项

        self.resize(300,45)

    def resize(self, *args) -> None:
        if len(args) == 1 and isinstance(args[0],QSize):
            self.w = args[0].width(),args[0].height()
        else:
            self.w,self.h = args[0],args[1]

        self.degree = (self.w-self.edge_distance_x*4)/self.max_value
        super().resize(self.w,self.h)

    def setText(self,text:str):
        self.text = text

    def isHideText(self,b:bool):
        self.__is_hide_text = b

    def setValue(self,v:int):
        self.cu_value = self.degree * v
        self.update()
        # 进度文字
        self.text = "{}%".format(v)
        # 发送信号
        self.valueChange.emit(v)

    def value(self) -> int:
        return self.cu_value // self.degree

    def __set_outerRadius(self,r:int):
        self._outer_radius = r

    def get_outerRadius(self)->int:
        return self._outer_radius
    
    def __set_innerRadius(self,r:int):
        self._inner_radius = r

    def get_innerRadius(self)->int:
        return self._inner_radius

    # 进度条
    def drawBar(self,painter:QPainter):
        painter.setPen(QPen(self.outline_border_color,self.get_borderWidth()))
        painter.drawRoundedRect(self.edge_distance_x,2,self.w-(self.edge_distance_x<<1),self.h-4,
                                self.get_outerRadius(),self.get_outerRadius())

        painter.setBrush(self.bar_color)
        painter.setPen(QPen(self.bar_color, 1))

        painter.drawRoundedRect(self.edge_distance_x+5, 2+6, self.cu_value, self.h - 4-12,
                             self.get_innerRadius(),self.get_innerRadius())

    # 绘制文字
    def drawText_(self,painter:QPainter):
        if not self.__is_hide_text:
            # 绘制文字
            f = QFont()
            f.setBold(True)
            f.setPointSize(self.get_fontSize())
            painter.setFont(f)
            painter.setPen(self.get_color())
            # 文字
            fs = textSize(f,self.text)
            fw = fs.width()
            fh = fs.height()
            painter.drawText(self.w // 2 - fw // 2,self.h // 2 + fh // 4, self.text)

    def paintEvent(self, event:QPaintEvent) -> None:
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)

        # 绘制进度条
        self.drawBar(painter)

        # 绘制文字
        self.drawText_(painter)

        painter.end()

    def resizeEvent(self, e:QResizeEvent) -> None:
        self.w = e.size().width()
        self.h = e.size().height()
        super().resizeEvent(e)

    # 专属样式
    '''
    outerRadius --> 进度条的外圆角大小
    innerRadius --> 进度条的外内角大小
    '''
    outerRadius = pyqtProperty(int,fset=__set_outerRadius,fget=get_outerRadius)
    innerRadius = pyqtProperty(int,fset=__set_innerRadius,fget=get_innerRadius)