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
    QResizeEvent
)

'''
    滑块
'''


class Slider(Widget):
    valueChanged = Signal(int)
    buffValueChanged = Signal(int) # 缓冲值信号

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # 图标
        self.icon_rect = QRect(0, 0, 25, 25)

        # 进度条高度
        self.slider_h = 8

        # 流动层的宽度
        self.flow_w = 0
        self.__flow_bg = QColor(253, 52, 62)

        # 缓冲层的宽度
        self.buff_w = 0
        self.__buff_bg = QColor(124, 123, 125)

        # 图标
        self.__icon_bg = QColor(230, 40, 50)

        # 流动层与图标的衔接处的插值
        self.flow_and_icon = 5

        # 最大/最小值
        self.max_value ={"max":0,"min":0}
        self.segv = 1 # 段值

        # 最大百分比
        self.max_percentage = 100

    def resize(self, *args) -> None:
        if len(args) == 1 and isinstance(args[0],QSize):
            super().resize(QSize(args[0].width(),args[1].height()+10))
        else:
            super().resize(args[0]+self.icon_rect.width(),args[1])
        print(self.size())

    def setFixedSize(self, *args) -> None:
        if len(args) == 1 and isinstance(args[0],QSize):
            super().setFixedSize(QSize(args[0].width(),args[1].height()))
        else:
            super().setFixedSize(args[0]+self.icon_rect.width(),args[1])


    # 图标运动
    def __movement(self,event):
        ex = event.x()
        w = self.width() - self.icon_rect.width()
        if ex >= 0 and ex <= w:
            self.flow_w = ex
            self.icon_rect.setRect(ex,
                                   self.icon_rect.y(),
                                   self.icon_rect.width(),
                                   self.icon_rect.height())
            self.valueChanged.emit(int(ex*self.segv))
            self.repaint()

    def mousePressEvent(self, event) -> None:
        self.__movement(event)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        self.__movement(event)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        super().mouseReleaseEvent(event)

    # --------------------------------------
    def __set_BuffBackgroundColor(self,color:QColor):
        self.__buff_bg = color

    def get_BuffBackgroundColor(self)->QColor:
        return self.__buff_bg
    
    def __set_FlowBackgroundColor(self,color:QColor):
        self.__flow_bg = color
    
    def get_FlowBackgroundColor(self)->QColor:
        return self.__flow_bg

    def __set_IconBackgroundColor(self,color:QColor):
        self.__icon_bg = color

    def get_IconBackgroundColor(self)->QColor:
        return self.__icon_bg

    def __set_sliderH(self,h:int):
        self.slider_h = h

    def get_sliderH(self) -> int:
        return self.slider_h

    def __set_iconSize(self,size:int):
        w = self.width()-self.icon_rect.width()  # 这句话的位置必须在最前面
        self.icon_rect.setRect(self.icon_rect.x(),
                               self.icon_rect.y(),
                               size,size)
        self.resize(w,self.height())
        # self.setFixedSize(w,self.height())

    # --------------------------------------
    def setValue(self,v:int):
        w = self.width()-self.icon_rect.width()
        if not self.max_value["max"] and v <= w:
            self.flow_w = v
        elif self.max_value["max"] and v <= self.max_value["max"]:
            self.flow_w = int(v/self.max_value["max"]*self.width())
        else:
            self.flow_w = w
        self.icon_rect.setRect(self.flow_w,self.icon_rect.y(),
                               self.icon_rect.width(),
                               self.icon_rect.width())
        self.update()

    # 设置百分比值
    def setPercentageValue(self,v:int):
        if v < 0:
            v = 0
        self.setValue(int(self.width()*v/self.max_percentage))

    # 设置缓冲值
    def setBuffValue(self,v:int):
        if v <= 0:
            return

        w = self.width()
        if not self.max_value["max"] and v <= w:
            self.buff_w = v
        elif self.max_value["max"] and v <= self.max_value["max"]:
            self.buff_w = int(v / self.max_value["max"] * self.width())
        else:
            self.buff_w = w

        self.buffValueChanged.emit(self.getBuffValue())
        self.buff_w += self.icon_rect.width()-10
        self.repaint()

    # 设置缓冲百分比值
    def setBuffPercentageValue(self,v:int):
        self.setBuffValue(int((self.width()-self.icon_rect.width())*v/self.max_percentage))

    def setMaxValue(self,max_v:int):
        self.max_value["max"] = max_v
        self.setValue(self.getValue()) # 重新调整滑块的当前值
        self.segv = max_v/(self.width()-self.icon_rect.width())

    # 获取值
    def getValue(self)->int:
        return int(self.flow_w*self.segv)

    # 返回百分比值
    def getPercentageValue(self):
        return int(self.flow_w*self.segv/(self.width()-self.icon_rect.width())*self.max_percentage)

    # 获取缓冲值
    def getBuffValue(self)->int:
        return self.buff_w

    def centerH(self) -> int:
        return self.height()//2

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
        print(self.icon_rect.x())
        rect = QRect(self.icon_rect.x(),
                     self.centerH()-self.icon_rect.height()//2+self.get_sliderH()//2,
                     self.icon_rect.width(),
                     self.icon_rect.height())
        painter.drawRoundedRect(rect,rect.width()//2,rect.height()//2)

    # 流动层(真实的一层)
    def drawFlowColor(self,painter:QPainter):
        if self.flow_w:
            self.__drawRoundedRect(painter,self.get_FlowBackgroundColor(),
                                   self.flow_w+self.flow_and_icon,
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

    '''
    自定义缓冲区颜色
    自定义流动层颜色
    自定义滑块背景高度
    自定义图标大小
    '''
    buffBgColor = pyqtProperty(QColor,fset=__set_BuffBackgroundColor,fget=get_BuffBackgroundColor)
    flowBackgroundColor = pyqtProperty(QColor,fset=__set_FlowBackgroundColor,fget=get_FlowBackgroundColor)
    iconBackgroundColor = pyqtProperty(QColor,fset=__set_IconBackgroundColor,fget=get_IconBackgroundColor)
    sliderH = pyqtProperty(int,fset=__set_sliderH,fget=get_sliderH)
    iconSize = pyqtProperty(int,fset=__set_iconSize,fget=None)


    def resizeEvent(self, e: QResizeEvent) -> None:
        self.segv = self.max_value["max"] / (e.size().width() - self.icon_rect.width())
        super().resizeEvent(e)
        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Slider()
    win.show()
    win.setStyleSheet('''
qproperty-backgroundColor:rgb(200, 200, 200);
qproperty-sliderH:8;
    ''')

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())