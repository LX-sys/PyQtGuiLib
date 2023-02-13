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
    pyqtProperty
)

'''
    滑块
'''


class Slider(Widget):
    valueChanged = Signal(int)

    def __init__(self,*args,**kwargs):
        # 图标
        self.icon_rect = QRect(0, 0, 25, 25)

        super().__init__(*args,**kwargs)
        self.resize(600,50)

        # 进度条高度
        self.slider_h = 15

        # 流动层的宽度
        self.flow_w = 0
        self.__flow_bg = QColor(253, 52, 62)

        # 缓冲层的宽度
        self.buff_w = 180
        self.__buff_bg = QColor(124, 123, 125)

        # 图标
        self.__icon_bg = QColor(230, 40, 50)

    def resize(self, *args) -> None:
        if len(args) == 1 and isinstance(args[0],QSize):
            super().resize(QSize(args[0].width(),args[1].height()+10))
        else:
            print(self.icon_rect.width())
            super().resize(args[0]+self.icon_rect.width()-self.get_margin(),args[1])

    def mousePressEvent(self, event) -> None:
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        ex = event.x()
        w = self.width()-self.icon_rect.width()+self.get_margin()
        if ex > -1 and ex < w:
            self.flow_w = ex
            self.icon_rect.setRect(ex,
                                   self.icon_rect.y(),
                                   self.icon_rect.width(),
                                   self.icon_rect.height())
            self.valueChanged.emit(ex)
            self.repaint()
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

    def get_sliderH(self)->int:
        return self.slider_h

    def __set_iconSize(self,size:int):
        # self.resize(self.width()-size,self.height())
        self.icon_rect.setRect(self.icon_rect.x(),
                               self.icon_rect.y(),
                               size,size)

    # --------------------------------------
    def setValue(self,v:int):
        self.flow_w = v
        self.icon_rect.setX(v)
        self.update()

    # 设置百分比值
    def setPercentageValue(self,v:int):
        self.setValue(int(self.width()*v/100))

    # 设置缓冲值
    def setBuffValue(self,v:int):
        self.buff_w = v
        self.update()

    # 设置缓冲百分比值
    def setBuffPercentageValue(self,v:int):
        self.setBuffValue(int(self.width()*v/100))

    def centerH(self) -> int:
        return self.height()//2

    # 绘制图标
    def drawIcon(self,painter:QPainter):
        # op = QPen()
        # op.setColor(qt.gray)
        # painter.setPen(op)
        bru = QBrush(self.get_IconBackgroundColor())
        painter.setBrush(bru)

        rect = QRect(self.get_margin()+self.icon_rect.x(),
                     self.centerH()-self.icon_rect.height()//2+self.get_sliderH()//2,
                     self.icon_rect.width()-self.get_margin()*2,
                     self.icon_rect.height()-self.get_margin()*2)
        painter.drawRoundedRect(rect,rect.width()//2,rect.height()//2)

    # 流动层(真实的一层)
    def drawFlowColor(self,painter:QPainter):
        if self.flow_w:
            bru = QBrush(self.get_FlowBackgroundColor())
            painter.setBrush(bru)

            painter.drawRoundedRect(self.get_margin(), self.centerH(),
                                    self.flow_w+5, self.get_sliderH() - self.get_margin() * 2,
                                    self.get_radius(), self.get_radius())

    # 缓冲层
    def drawBuffBgColor(self,painter:QPainter):
        if self.buff_w:
            bru = QBrush(self.get_BuffBackgroundColor())
            painter.setBrush(bru)
            painter.drawRoundedRect(self.get_margin(), self.centerH(),
                                    self.buff_w - self.get_margin() * 2, self.get_sliderH() - self.get_margin() * 2,
                                    self.get_radius(), self.get_radius())

    # 底色
    def drawBackgroundColor(self,painter:QPainter):
        bru = QBrush(self.get_backgroundColor())
        painter.setBrush(bru)
        painter.drawRoundedRect(self.get_margin(),self.centerH(),
                                self.width()-self.get_margin()*2,self.get_sliderH()-self.get_margin()*2,
                                self.get_radius(),self.get_radius())

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


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Slider()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())