# -*- coding:utf-8 -*-
# @time:2022/12/2710:45
# @author:LX
# @file:gradientBar.py
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
    QLinearGradient,
    QBrush,
    Signal,
    qt
)
'''
    线性渐变进度条
'''

class GradientBar(QWidget):
    # 进度改变时,发出信号
    valueChange = Signal(int)
    
    def __init__(self,*args,**kwargs):
        self.max_value = 100 # 进度条最大百分比值
        super().__init__(*args,**kwargs)

        self.w,self.h = 800,50
        self.resize(self.w,self.h)

        self.degree = round(self.w / self.max_value, 2)

        # 进度条真实长度
        self.bw = 0

        # 当前进度条的百分比值
        self.cu_value = 0

        # 渐变颜色列表
        '''
            [(颜色比重0-1,QColor()),...]
        '''
        self.line_color_lists = []

        # 圆角半径
        self.radius = 0

        self.setValue(100)

        # 进度条底色
        self.bg_color = QColor(211, 211, 211)

        self.setColorAts(
            [(0.2,QColor(170, 170, 255)),(0.4, QColor(170, 255, 127)),(0.6, QColor(85, 170, 127))]
             )

    # 设置颜色比重和颜色
    def setColorAts(self,colors:list):
        '''

        :param colors:  [(颜色比重0-1,QColor()),...]
        :return:
        '''
        self.line_color_lists = colors

    # 设置背景底色
    def setBackGroundColor(self,bg_color:QColor):
        self.bg_color = bg_color

    # 添加一种颜色
    def appendColor(self,color:tuple):
        '''

        :param color: (颜色比重0-1,QColor())
        :return:
        '''
        self.line_color_lists.append(color)

    # 移除一种颜色
    def removeColor(self,color:tuple):
        '''

        :param color: (颜色比重0-1,QColor())
        :return:
        '''
        self.line_color_lists.remove(color)

    # 返回所有的颜色和比重
    def getColors(self) -> list:
        return self.line_color_lists

    def setValue(self,value:int):
        self.cu_value = value
        self.bw = int(self.degree*value)
        
        self.update()
        self.valueChange.emit(value)
        
    def value(self) -> int:
        return self.cu_value

    # 设置圆角半径
    def setRadius(self,r:int):
        self.radius = r

    def resize(self, *args) -> None:
        if len(args) == 1 and isinstance(args[0],QSize):
            self.w = args[0].width(),args[0].height()
        else:
            self.w,self.h = args[0],args[1]

        self.degree = round(self.w/self.max_value,2)
        super().resize(self.w,self.h)

    # 渐变进度条
    def gradientBar(self,painter:QPainter):
        # 进度条颜色渐变
        gradient = QLinearGradient(0, 0, self.w, self.h)
        for proportion,color in self.line_color_lists:
            gradient.setColorAt(proportion,color)

        # 进度条底色
        bg = QBrush(self.bg_color)

        painter.setPen(qt.NoPen)  # 设置无画笔
        painter.setBrush(bg)
        painter.drawRoundedRect(0, 0, self.w, self.h,self.radius,self.radius)
        painter.setBrush(gradient)
        painter.drawRoundedRect(0, 0, self.bw, self.h, self.radius,self.radius)

    def paintEvent(self, e:QPaintEvent) -> None:
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)

        # 渐变进度条
        self.gradientBar(painter)

        painter.end()

    def resizeEvent(self, e:QResizeEvent) -> None:
        self.w = e.size().width()
        self.h = e.size().height()

        self.degree = round(self.w/self.max_value,2)
        self.setValue(self.value())
        super().resizeEvent(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = GradientBar()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())