from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,sys,
    Signal,
    Widget,
    QPainter,
    QColor,
    QBrush,
    QPen,
    qt,
    QRect,
    QSize,
    pyqtProperty,
    QResizeEvent,
    QMouseEvent
)

class Slider(Widget):
    valueChanged = Signal(int)
    buffValueChanged = Signal(int) # 缓冲值信号

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(300,50)

        # 图标
        self.icon_rect = QRect(150, 0, 25, 25)
        self.proportion_x = self.icon_rect.x()/self.width() # 位置与宽度的比例

        # 进度条高度
        self.slider_h = 8

        # 流动层的宽度
        self.flow_w = 0
        self.__flow_bg = QColor(253, 52, 62)

        # 缓冲层的宽度
        self.buff_w = 0
        self.__buff_bg = QColor(124, 123, 125)
        self.buff_proportion_x = self.buff_w/self.width() # 缓冲位置与宽度的比例

        # 图标
        self.__icon_bg = QColor(230, 40, 50)

        # 流动层与图标的衔接处的插值
        self.flow_and_icon = 5

        # 最大/最小值
        self.max_value ={"max":100,"min":0}

    def setMaxValue(self,v):
        self.max_value["max"] = v

    def getMaxValue(self)->int:
        return self.max_value["max"]

    def getValue(self) -> int:
        return int(self.icon_rect.x() / self.width() * self.getMaxValue())

    def setValue(self,v:int):
        self.proportion_x = v / self.width()  # 再窗口变化时,记录位置与宽度的比例,
        '''
            总宽度: 300  运动值:x   未知
            最大值: 250  v:100
        '''
        self.icon_rect.setRect(int(v/self.getMaxValue()*self.width()),
                               self.icon_rect.y(),
                               self.icon_rect.width(),
                               self.icon_rect.height())

        self.repaint()

    # 设置缓冲值
    def setBuffValue(self, v: int):
        self.buff_proportion_x = v / self.width()  # 缓冲位置与宽度的比例
        self.buff_w = int(v/self.getMaxValue()*self.width())
        self.repaint()

    # -------------------------
    def __set_BuffBackgroundColor(self, color: QColor):
        self.__buff_bg = color

    def get_BuffBackgroundColor(self) -> QColor:
        return self.__buff_bg

    def __set_FlowBackgroundColor(self, color: QColor):
        self.__flow_bg = color

    def get_FlowBackgroundColor(self) -> QColor:
        return self.__flow_bg

    def __set_IconBackgroundColor(self, color: QColor):
        self.__icon_bg = color

    def get_IconBackgroundColor(self) -> QColor:
        return self.__icon_bg

    def __set_sliderH(self,h:int):
        self.slider_h = h

    def get_sliderH(self) -> int:
        return self.slider_h

    def __set_iconSize(self, size: int):
        self.icon_rect.setRect(self.icon_rect.x(),
                               self.icon_rect.y(),
                               size,size)

    # --------------------------------
    def centerH(self) -> int:
        return self.height()//2

    # 图标运动
    def __movement(self,e):
        x = e.x()
        if x >= 0 and x <= self.width():
            self.icon_rect.setRect(x,
                                   self.icon_rect.y(),
                                   self.icon_rect.width(),
                                   self.icon_rect.height())
            '''
                总宽度: 300  运动值:x   150
                最大值: 250
            '''
            self.proportion_x = x / self.width()  # 再窗口变化时,记录位置与宽度的比例,
            self.valueChanged.emit(self.getValue())
            self.flow_w = self.icon_rect.x()  # 设置流动层
            self.repaint()

    def mousePressEvent(self, e:QMouseEvent) -> None:
        self.__movement(e)
        super().mousePressEvent(e)

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        self.__movement(e)
        super().mouseMoveEvent(e)

    def __drawRoundedRect(self,painter:QPainter,brush_color:QColor,w:int,h:int):
        bru = QBrush(brush_color)
        painter.setBrush(bru)
        rect = QRect(0, self.centerH(),w,h)
        painter.drawRoundedRect(rect,self.get_radius(), self.get_radius())

    # 绘制图标
    def drawIcon(self,painter:QPainter):
        # op = QPen()
        # op.setColor(qt.gray)
        # painter.setPen(op)
        bru = QBrush(self.get_IconBackgroundColor())
        painter.setBrush(bru)
        rect = QRect(self.icon_rect.x(),
                     self.centerH()-self.icon_rect.height()//2+self.get_sliderH()//2,
                     self.icon_rect.width(),
                     self.icon_rect.height())
        painter.drawRoundedRect(rect,rect.width()//2,rect.height()//2)

    # 流动层(真实的一层)
    def drawFlowColor(self,painter:QPainter):
        self.__drawRoundedRect(painter,self.get_FlowBackgroundColor(),
                               self.icon_rect.x()+self.flow_and_icon,
                               self.get_sliderH())

    # 缓冲层
    def drawBuffBgColor(self,painter:QPainter):
        if self.buff_w:
            self.__drawRoundedRect(painter,self.get_BuffBackgroundColor(),
                                   self.buff_w,
                                   self.get_sliderH())

    # 底色
    def drawBackgroundColor(self,painter:QPainter):
        self.__drawRoundedRect(painter,self.get_backgroundColor(),
                               self.width(),
                               self.get_sliderH())

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform)

        painter.setPen(qt.NoPen)
        self.drawBackgroundColor(painter)
        self.drawBuffBgColor(painter)
        self.drawFlowColor(painter)
        self.drawIcon(painter)

        painter.end()

    def resizeEvent(self, e: QResizeEvent) -> None:
        self.icon_rect.setRect(int(self.proportion_x * self.width()),
                               self.icon_rect.y(),
                               self.icon_rect.width(),
                               self.icon_rect.height())

        self.buff_w = int(self.buff_proportion_x * self.width())

    '''
        自定义缓冲区颜色
        自定义流动层颜色
        自定义滑块背景高度
        自定义图标大小
    '''
    buffBgColor = pyqtProperty(QColor, fset=__set_BuffBackgroundColor, fget=get_BuffBackgroundColor)
    flowBackgroundColor = pyqtProperty(QColor, fset=__set_FlowBackgroundColor, fget=get_FlowBackgroundColor)
    iconBackgroundColor = pyqtProperty(QColor, fset=__set_IconBackgroundColor, fget=get_IconBackgroundColor)
    sliderH = pyqtProperty(int, fset=__set_sliderH, fget=get_sliderH)
    iconSize = pyqtProperty(int, fset=__set_iconSize, fget=None)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Slider()
    win.show()
    win.setStyleSheet('''
qproperty-radius:4;
qproperty-backgroundColor:rgb(200, 200, 200);
qproperty-sliderH:8;
    ''')

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())