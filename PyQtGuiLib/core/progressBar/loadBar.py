# -*- coding:utf-8 -*-
# @time:2022/12/2214:52
# @author:LX
# @file:loadBar.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QWidget,
    Signal,
    QFont,
    QColor,
    QPen,
    QPainter,
    QPaintEvent,
    QFontMetricsF,
    QSize,
    QResizeEvent,
    qt,
    textSize
)


'''
    加载进度条
'''
class LoadBar(QWidget):
    # 进度改变时,发出信号
    valueChange = Signal(int)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.w,self.h =30, 50

        self.edge_distance_x = 5  # 水平方向的边距
        self.outer_radius,self.inner_radius = 20, 15 # 内外圆角

        # 每一段大小
        self.degree = (self.w-self.edge_distance_x*4)/100
        # 当前值
        self.cu_value = 0
        self.max_value = 100

        # 外框和进度条的颜色
        self.outline_border_color = QColor(0,0,0)
        self.bar_color = QColor(0,82,70)

        # 边的宽度
        self.border_width = 3

        # 文字属性
        self.text = "100%"
        self.text_size = 15
        self.text_color = QColor(170, 85, 127)
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

    def setValue(self,v:int):
        self.cu_value = self.degree * v
        self.update()
        # 进度文字
        self.text = "{}%".format(v)
        # 发送信号
        self.valueChange.emit(v)

    def value(self) -> int:
        return self.cu_value // self.degree

    # 设置进度条的外圆角大小
    def setOuterRadius(self,r:int):
        self.outer_radius = r

    # 设置进度条的内圆角大小
    def setInnerRadius(self,r:int):
        self.inner_radius = r

    # 设置进度条的内外圆角
    def setRadius(self,outer_r:int,inner_r:int):
        self.setOuterRadius(outer_r)
        self.setInnerRadius(inner_r)

    # 设置进度条边的宽
    def setBorderWidth(self,w:int):
        self.border_width = w

    # 进度条
    def drawBar(self,painter:QPainter):
        painter.setPen(QPen(self.outline_border_color,self.border_width))
        painter.drawRoundedRect(self.edge_distance_x,2,self.w-(self.edge_distance_x<<1),self.h-4,
                                self.outer_radius,self.outer_radius)

        painter.setBrush(self.bar_color)
        painter.setPen(QPen(self.bar_color, 1))

        painter.drawRoundedRect(self.edge_distance_x+5, 2+6, self.cu_value, self.h - 4-12,
                             self.inner_radius,self.inner_radius)

    # 绘制文字
    def drawText_(self,painter:QPainter):
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = LoadBar()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())