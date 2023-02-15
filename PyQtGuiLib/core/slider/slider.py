from PyQt5 import QtGui

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
        self.__bgH = 8

        # 图标位置/大小,百分比位置
        self.icon_x = self.leftMargin()
        self.icon_size = QSize(15,15)
        self.icon_pre_pos = 0

        # 流动层
        self.flow_w = 0

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

        # 返回值保存
        self.re_flow_v = 0
        self.re_buff_v = 0

        # 图标是否具有 hover 效果
        self.__isHoverStart = False
        self.__isHover = False

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
    
    def __set_bgHeight(self,h:int):
        self.__bgH = h

    # ----------------------------

    def setHoverIcon(self,b:bool):
        self.__isHoverStart = b

    def getMaxValue(self) -> int:
        return self.max_value

    def setMaxValue(self,v):
        self.max_value = v

    # 设置当前值
    def setValue(self,v:int):
        if not v:
            self.buff_w = 0
            return

        x = self.valueToPos(v)
        self.icon_pre_pos = (x - self.leftMargin()) / (self.width() - self.rightMargin())
        self.flow_w = self.valueToPos(v)+self.icon_size.width()//2

    def getValue(self) -> int:
        if not self.flow_w:
            return 0

        return int(self.posToValve(self.flow_w-self.icon_size.width()//2))

    # 设置缓冲值
    def setBuffValue(self,v:int):
        if not v:
            self.buff_w = 0
            return

        x = self.valueToPos(v)
        self.buff_pre_pos = (x - self.leftMargin()) / (self.width() - self.rightMargin())
        self.buff_w = self.valueToPos(v)

    def getBuffValue(self)->int:
        if not self.flow_w:
            return 0

        return int(self.posToValve(self.buff_w))

    def leftMargin(self) -> int:
        return self.margin

    def rightMargin(self) -> int:
        return self.leftMargin() << 1

    def centerH(self) -> int:
        return self.height()//2 - self.__bgH//2

    # 坐标值 转 百分比值
    def posToValve(self,x:int) -> float:
        '''
            总宽度: self.width()  当前坐标值:x
            最大值 getMaxValue()  ?
        '''
        w = self.width()-self.rightMargin()
        return x/w*self.getMaxValue()

    # 百分比 转 坐标值
    def valueToPos(self,v:int) -> float:
        '''
            总宽度: self.width()  ?
            最大值 getMaxValue()  当前百分比值 v
        '''
        w = self.width()-self.rightMargin()
        return v/self.getMaxValue()*w

    def __mouse(self,event:QMouseEvent):
        x = event.x()
        w = self.width() - self.leftMargin()
        if x >= self.leftMargin() and x <= w:
            # 记录图标的百分比值
            self.icon_pre_pos = (x-self.leftMargin())/(self.width()-self.rightMargin())
            # print("输出值:",self.posToValve(x - self.leftMargin()))
            self.valueChanged.emit(int(self.posToValve(x - self.leftMargin())))
            # 更新流动层
            self.flow_w = x + self.icon_size.width()//2
            # 图标位置
            self.icon_x = x
            self.update()

    def leaveEvent(self, e) -> None:
        if self.__isHoverStart:
            self.__isHover = False
            self.update()

    def enterEvent(self, e) -> None:
        if self.__isHoverStart:
            self.__isHover = True
            self.update()

    def mousePressEvent(self, event:QMouseEvent) -> None:
        self.__mouse(event)

    def mouseMoveEvent(self, event:QMouseEvent) -> None:
        self.__mouse(event)

    def __drawRoundedRect(self,painter:QPainter,brush_color:QColor,w:int):
        bru = QBrush(brush_color)
        painter.setBrush(bru)
        if w - self.rightMargin() < 0:
            rect = QRect(self.leftMargin(), self.centerH(), w, self.__bgH)
        else:
            rect = QRect(self.leftMargin(), self.centerH(), w - self.rightMargin(), self.__bgH)

        painter.drawRoundedRect(rect,self.get_radius(), self.get_radius())

    # 绘制图标
    def drawIcon(self,painter:QPainter):
        if self.__isHoverStart is False or self.__isHover:
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

    # 流动层
    def drawFlowColor(self,painter:QPainter):
        self.__drawRoundedRect(painter,self.get_flowColor(),
                               int(self.flow_w))

    # 缓冲层
    def drawBuffBgColor(self,painter:QPainter):
        self.__drawRoundedRect(painter,self.get_buffColor(),
                               int(self.buff_w))

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
        if self.flow_w:
            self.flow_w = self.icon_x + self.icon_size.width()//2

    # 自定义属性
    bgColor = pyqtProperty(QColor,fset=__set_bgColor,fget=get_bgColor)
    buffColor = pyqtProperty(QColor,fset=__set_buffColor,fget=get_buffColor)
    flowColor = pyqtProperty(QColor,fset=__set_flowColor,fget=get_flowColor)
    iconColor = pyqtProperty(QColor,fset=__set_iconColor,fget=get_iconColor)
    iconSize = pyqtProperty(int,fset=__set_iconSize,fget=None)
    bgHeight = pyqtProperty(int,fset=__set_bgHeight,fget=None)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#
#     win = Slider()
#     win.show()
#     win.setMaxValue(200)
#     win.setValue(100)
#     print(win.getValue())
#     # win.setBuffValue(46)
#     # print(win.getBuffValue())
#     win.setStyleSheet('''
# qproperty-radius:4;
# qproperty-flowColor:rgb(100,50,50);
# qproperty-iconSize:15;
#     ''')
# #     win.setStyleSheet('''
# # qproperty-radius:4;
# # qproperty-backgroundColor:rgb(200, 200, 200);
# # qproperty-sliderH:8;
# #     ''')
#
#     if PYQT_VERSIONS in ["PyQt6","PySide6"]:
#         sys.exit(app.exec())
#     else:
#         sys.exit(app.exec_())