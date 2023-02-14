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
    QMouseEvent
)


class Slider(Widget):
    valueChanged = Signal(int)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,80)

        # 边距
        self.margin = 9

        # 背景高度
        self.bgH = 8

        # 图标位置/大小,百分比位置
        self.icon_x = self.leftMargin()
        self.icon_size = QSize(15,15)
        self.icon_pre_pos = 0

        # 流动层
        self.flow_w = self.icon_x

        # 缓冲层,百分比位置
        self.buff_w = 0
        self.buff_pre_pos = 0

        # 最大值
        self.max_value = 100

        # -----
        self.__bgColor = QColor(200,200,200)
        self.__buffColor = QColor(100,100,100)
        self.__flowColor = QColor(200,100,200)
        self.__iconColor = QColor(230, 40, 50)
        # -----

    # ----------------------------
    def __set_bgColor(self,color:QColor):
        self.__bgColor = color

    def get_bgColor(self)->QColor:
        return self.__bgColor

    def __set_buffColor(self, color: QColor):
        self.__buffColor = color

    def get_buffColor(self) -> QColor:
        return self.__buffColor

    def __set_flowColor(self, color: QColor):
        self.__flowColor = color

    def get_flowColor(self) -> QColor:
        return self.__flowColor

    def __set_iconColor(self, color: QColor):
        self.__iconColor = color

    def get_iconColor(self) -> QColor:
        return self.__iconColor

    def __set_iconSize(self,size:int):
        self.icon_size = QSize(size,size)

    # ----------------------------

    def getMaxValue(self) -> int:
        return self.max_value

    def setMaxValue(self,v):
        self.max_value = v

    # 设置当前值
    def setValue(self,v:int):
        x = self.valueToPos(v)
        self.icon_pre_pos = (x - self.leftMargin()) / (self.width() - self.rightMargin())
        self.flow_w = self.valueToPos(v)+self.icon_size.width()//2

    # 设置缓冲值
    def setBuffValue(self,v:int):
        x = self.valueToPos(v)
        self.buff_pre_pos = (x - self.leftMargin()) / (self.width() - self.rightMargin())
        self.buff_w = self.valueToPos(v)

    def leftMargin(self) -> int:
        return self.margin

    def rightMargin(self) -> int:
        return self.margin << 1

    def centerH(self) -> int:
        return self.height()//2 - self.bgH//2

    # 坐标值 转 百分比值
    def posToValve(self,x:int) -> int:
        '''
            总宽度: self.width()  当前坐标值:x
            最大值 getMaxValue()  ?
        '''
        w = self.width()-self.rightMargin()
        return int(x/w*self.getMaxValue())

    # 百分比 转 坐标值
    def valueToPos(self,v:int) -> int:
        '''
            总宽度: self.width()  ?
            最大值 getMaxValue()  当前百分比值 v
        '''
        return int(v/self.getMaxValue()*self.width())

    def __mouse(self,event:QMouseEvent):
        x = event.x()
        w = self.width() - self.leftMargin()
        if x >= self.leftMargin() and x < w:
            print(self.posToValve(x-self.leftMargin()))
            self.valueChanged.emit(self.posToValve(x-self.leftMargin()))
            # 记录图标的百分比值
            self.icon_pre_pos = (x-self.leftMargin())/(self.width()-self.rightMargin())
            # 更新流动层
            self.flow_w = x + self.icon_size.width()//2
            # 图标位置
            self.icon_x = x
            self.update()

    def mousePressEvent(self, event:QMouseEvent) -> None:
        self.__mouse(event)

    def mouseMoveEvent(self, event:QMouseEvent) -> None:
        self.__mouse(event)

    def __drawRoundedRect(self,painter:QPainter,brush_color:QColor,w:int):
        bru = QBrush(brush_color)
        painter.setBrush(bru)
        rect = QRect(self.leftMargin(), self.centerH(),w-self.rightMargin(),self.bgH)
        painter.drawRoundedRect(rect,self.get_radius(), self.get_radius())

    # 绘制图标
    def drawIcon(self,painter:QPainter):
        bru = QBrush(self.get_iconColor())
        painter.setBrush(bru)

        icon_w = self.icon_size.width()
        icon_h = self.icon_size.height()
        y = self.height()//2-icon_w//2
        rect = QRect(self.icon_x-icon_w//2,
                     y,
                     icon_w,
                     icon_h)
        painter.drawRoundedRect(rect,icon_w//2,icon_h//2)

    # 流动层(真实的一层)
    def drawFlowColor(self,painter:QPainter):
        self.__drawRoundedRect(painter,self.get_flowColor(),
                               self.flow_w)

    # 缓冲层
    def drawBuffBgColor(self,painter:QPainter):
        if self.buff_w:
            self.__drawRoundedRect(painter,self.get_buffColor(),
                                   self.buff_w)

    # 底色
    def drawBackgroundColor(self,painter:QPainter):
        self.__drawRoundedRect(painter,self.get_bgColor(),
                               self.width())


    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform)

        painter.setPen(qt.NoPen)

        self.__update()
        # ------------------------------
        self.drawBackgroundColor(painter)
        self.drawBuffBgColor(painter)
        self.drawFlowColor(painter)
        self.drawIcon(painter)

        painter.end()

    # 更新
    def __update(self):
        # 更新缓冲层
        self.buff_w = int(self.buff_pre_pos*(self.width()-self.rightMargin()))+self.leftMargin()
        # 更新图标位置
        self.icon_x = int(self.icon_pre_pos*(self.width()-self.rightMargin()))+self.leftMargin()
        # 更新流动层
        self.flow_w = self.icon_x + self.icon_size.width()//2

    bgColor = pyqtProperty(QColor,fset=__set_bgColor,fget=get_bgColor)
    buffColor = pyqtProperty(QColor,fset=__set_buffColor,fget=get_buffColor)
    flowColor = pyqtProperty(QColor,fset=__set_flowColor,fget=get_flowColor)
    iconColor = pyqtProperty(QColor,fset=__set_iconColor,fget=get_iconColor)
    iconSize = pyqtProperty(int,fset=__set_iconSize,fget=None)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Slider()
    win.show()
    # win.setValue(90)
    win.setBuffValue(10)
    win.setStyleSheet('''
qproperty-radius:4;
qproperty-flowColor:rgb(100,50,50);
qproperty-iconSize:10;
    ''')
#     win.setStyleSheet('''
# qproperty-radius:4;
# qproperty-backgroundColor:rgb(200, 200, 200);
# qproperty-sliderH:8;
#     ''')

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())