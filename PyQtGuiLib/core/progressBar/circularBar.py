from PyQtGuiLib.header import (
    QWidget,
    Signal,
    Qt,
    QFont,
    QColor,
    QPen,
    QPainter,
    QPaintEvent,
    QSize,
    QResizeEvent,
    textSize,
    qt,
    pyqtProperty
)


from PyQtGuiLib.core.widgets import WidgetABC
'''
    圆环进度条
'''
class CircularBar(WidgetABC):
    # 进度改变时,发出信号
    valueChange = Signal(int)

    # 外圈/内圈
    OuterRing = "OuterRing"
    InnerRing = "InnerRing"
    Double = "Double"

    # 圈的风格
    SolidLine = qt.SolidLine
    DashLine = qt.DashLine
    DotLine = qt.DotLine
    DashDotLine = qt.DashDotLine
    DashDotDotLine = qt.DashDotDotLine
    CustomDashLine = qt.CustomDashLine


    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.w,self.h = 150,150
        self.degree = 3.6  # 每一段的大小
        self.outer_n = 0 # 总量
        self.inner_n = 0

        # 文字
        self.text = "0%"

        '''
            进度发生变化时,引起变化的线段,是外圈还是内圈
        '''
        self.variableLine = CircularBar.InnerRing

        self.__max_value = 100

        # 外圈/内圈 颜色
        self._outer_rgb = QColor(104, 167, 205)
        self._inner_rgb = QColor(117, 199, 255)

        # 外圈/内圈 线段样式
        self.outer_style = CircularBar.CustomDashLine
        self.inner_style = CircularBar.SolidLine

        # 外圈/内圈 线段长度
        self.outer_width = 10
        self.inner_width = 3

        # 外圈/内圈 自定义风格  只有当线段样式为 CircularBar.CustomDashLine 才有效
        self.outer_pattern = []
        self.inner_pattern = []

    def resize(self, *args) -> None:
        if len(args) == 1 and isinstance(args[0],QSize):
            self.w = args[0].width(),args[0].height()
        else:
            self.w,self.h = args[0],args[1]

        super().resize(self.w+10,self.h+10)

    def setText(self,text:str):
        self.text = text

    def __set_outerColor(self,color:QColor):
        self._outer_rgb = color

    def get_outerColor(self)->QColor:
        return self._outer_rgb

    def __set_innerColor(self,color:QColor):
        self._inner_rgb = color

    def get_innerColor(self)->QColor:
        return self._inner_rgb

    # 设置外圈风格
    def setOuterStyle(self,style):
        self.outer_style = style

    # 设置内圈风格
    def setInnerStyle(self,style):
        self.inner_style = style

    # 设置变化的线段
    def setVariableLineSegment(self,mode):
        self.variableLine = mode

    def setValue(self,v:int):
        if v > self.__max_value:
            raise ValueError("The maximum is 100 !")

        if self.variableLine == CircularBar.OuterRing:
            self.outer_n = int(self.degree*v)
            self.inner_n = 360
        elif self.variableLine == CircularBar.InnerRing:
            self.outer_n = 360
            self.inner_n = int(self.degree*v)
        elif self.variableLine == CircularBar.Double:
            self.outer_n = int(self.degree * v)
            self.inner_n = int(self.degree * v)

        self.text = "{}%".format(v)
        self.update()
        # 发射信号
        self.valueChange.emit(v)

    def value(self) -> int:
        return int(self.n/self.degree)

    def maxValue(self) -> int:
        return self.__max_value

    # 设置外圈自定义线段样式
    def setOuterDashPattern(self,pattern:list):
        self.outer_pattern = pattern

    # 设置内圈自定义线段样式
    def setInnerDashPattern(self,pattern:list):
        self.inner_pattern = pattern

    # 画环
    def drawLoopBar(self,painter:QPainter,x,y):
        inner_x,inner_y = x+10,y+10
        inner_w,inner_h = self.w-20,self.h-20

        # ------------
        outer_op = QPen(self.get_outerColor(),self.outer_width)
        outer_op.setStyle(self.outer_style)
        if self.outer_style == CircularBar.CustomDashLine:
            outer_op.setDashPattern(self.outer_pattern)
        painter.setPen(outer_op)
        painter.drawArc(x,y,self.w,self.h,0,self.outer_n*16)
        inner_op = QPen(self.get_innerColor(), self.inner_width)
        inner_op.setStyle(self.inner_style)
        if self.inner_style == CircularBar.CustomDashLine:
            inner_op.setDashPattern(self.inner_pattern)
        painter.setPen(inner_op)
        painter.drawArc(inner_x,inner_y,inner_w,inner_h, 0, self.inner_n * 16)
        # ---------------
        # 绘制文字
        f = QFont()
        f.setPointSize(self.get_fontSize())
        painter.setFont(f)
        painter.setPen(self.get_color())
        # 文字
        fs = textSize(f,self.text)
        fw = fs.width()
        fh = fs.height()
        painter.drawText(inner_x+inner_w//2-fw//2,y+self.h//2+fh//4,self.text)

    def paintEvent(self, event:QPaintEvent) -> None:
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)

        self.drawLoopBar(painter,6,6)

        painter.end()

    # 跟随窗口变化
    def resizeEvent(self, event:QResizeEvent) -> None:
        self.w,self.h = event.size().width()-13,event.size().height()-13
        super().resizeEvent(event)

    # 专属QSS
    '''
    outerColor --> 设置外圈颜色
    innerColor --> 设置内圈颜色
    '''
    outerColor = pyqtProperty(QColor,fset=__set_outerColor,fget=get_outerColor)
    innerColor = pyqtProperty(QColor,fset=__set_innerColor,fget=get_innerColor)