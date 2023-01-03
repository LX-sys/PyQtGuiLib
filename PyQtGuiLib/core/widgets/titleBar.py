
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QWidget,
    QFrame,
    QPainter,
    QPaintEvent,
    QRect,
    QPen,
    QFont,
    QFontMetricsF,
    QColor,
    QPushButton,
    QPropertyAnimation,
    QBrush,
    Qt
)

'''
    窗口的标题栏
'''


# 缩小,放大,关闭 三按钮基类
class ButtonIcon(QPushButton):

    '''
        缩小,放大,关闭
        win 风格
        mac 风格
    '''
    WinStyle = "WinStyle"
    MacStyle = "MacStyle"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.w,self.h = 20,20
        self.resize(self.w,self.h)
        
        self.btnStyle = ButtonIcon.MacStyle

        self.open_width = 1
        self.radius = 3

    # 设置 缩小,放大,关闭 的风格
    def setBtnStyle(self,style:str = "WinStyle"):
        self.btnStyle = style
    
    def isWinStyle(self)->bool:
        return True if self.btnStyle == ButtonIcon.WinStyle else False

    def isMacStyle(self)->bool:
        return True if self.btnStyle == ButtonIcon.MacStyle else False

    # 绘制图标,所有子类都必须实现都方法
    def drawIcon(self, painter: QPainter):
        pass

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(painter.Antialiasing | painter.SmoothPixmapTransform | painter.TextAntialiasing)

        self.drawIcon(painter)

        painter.end()


# 缩小按钮
class ZoomButton(ButtonIcon):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def drawIcon(self,painter:QPainter):
        op = QPen()
        op.setWidth(self.open_width)
        painter.setPen(op)

        if self.isWinStyle():
            rect = QRect(1,1,self.width()-self.open_width-1,self.height()-self.open_width-1)
            painter.drawRoundedRect(rect,self.radius,self.radius)
            painter.drawLine(5,self.height()//2,self.width()-5,self.height()//2)
        elif self.isMacStyle():
            brush = QBrush(QColor(255, 199, 124))
            painter.setBrush(brush)

            rect = QRect(1, 1, self.width() - self.open_width - 1, self.height() - self.open_width - 1)
            painter.drawRoundedRect(rect, self.w//2,self.h//2)
            painter.drawLine(5, self.height() // 2, self.width() - 5, self.height() // 2)
            painter.setBrush(Qt.NoBrush)


# 放大按钮
class LargeButton(ButtonIcon):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)


    def drawIcon(self, painter: QPainter):
        op = QPen()
        op.setWidth(self.open_width)
        painter.setPen(op)

        if self.isWinStyle():
            rect1 = QRect(1, 1, 13,13)
            rect2 = QRect(6, 6, 13,13)
            painter.drawRoundedRect(rect1, self.radius,self.radius)
            painter.drawRoundedRect(rect2, self.radius,self.radius)
        elif self.isMacStyle():
            brush = QBrush(QColor(40, 194, 50))
            painter.setBrush(brush)

            rect = QRect(1, 1, self.width() - self.open_width - 1, self.height() - self.open_width - 1)
            painter.drawRoundedRect(rect, self.w//2,self.h//2)

            brush = QBrush(QColor(0,0,0))
            painter.setBrush(brush)

            painter.drawEllipse(self.width()//2-5,self.height()//2-5,5,5)
            painter.drawEllipse(self.width()//2+1,self.height()//2+1,5,5)

            painter.setBrush(Qt.NoBrush)


# 关闭按钮
class CloseButton(ButtonIcon):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def drawIcon(self, painter: QPainter):
        op = QPen()
        op.setWidth(self.open_width)
        painter.setPen(op)

        if self.isWinStyle():
            rect = QRect(1,1,self.width()-self.open_width-1,self.height()-self.open_width-1)
            painter.drawRoundedRect(rect,self.radius,self.radius)
            painter.drawLine(5,5,self.width()-5,self.height()-5)
            painter.drawLine(self.width()-5,5,5,self.height()-5)
        elif self.isMacStyle():
            brush = QBrush(QColor(252, 70, 70))
            painter.setBrush(brush)

            rect = QRect(1, 1, self.width() - self.open_width - 1, self.height() - self.open_width - 1)
            painter.drawRoundedRect(rect, self.w//2,self.h//2)
            painter.drawLine(5, 5, self.width() - 5, self.height() - 5)
            painter.drawLine(self.width() - 5, 5, 5, self.height() - 5)


class TitleBar(QFrame):

    # 标题的位置
    Title_Left = "TextLeft"
    Title_Center = "TitleCenter"

    '''
        缩小,放大,关闭
        win 风格
        mac 风格
    '''
    WinStyle = "WinStyle"
    MacStyle = "MacStyle"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.__parent = None #  type:QWidget

        if args:
            self.__parent = args[0]

        # 标题位置
        self.title_pos = TitleBar.Title_Left

        # 标题高度
        self.h = 35
        # 标题文本
        self.title_text="Title"
        self.title_color = QColor(0,0,0)
        self.title_size = 20


        if self.__parent is not None:
            self.move(0,0)
            self.resize(self.__parent.width(),self.h)

        # 创建缩小,放大,关闭 按钮
        self.zm = ZoomButton(self)
        self.lm = LargeButton(self)
        self.cm = CloseButton(self)
        # 创建缩小,放大,关闭事件
        self.createEvent()

        # 设置标题设置
        self.setTitlePos(TitleBar.Title_Center)
        self.updateTitleSize()  # 更新标题栏位置

    def setTitleText(self,text:str):
        self.title_text = text

    def setTitleColor(self,color:QColor):
        self.title_color = color

    def setTitleSize(self,size:int):
        self.title_size = size

    def setAllTitle(self,text:str,color:QColor,size:int):
        self.setTitleText(text)
        self.setTitleColor(color)
        self.setTitleSize(size)

    # 设置标题的位置
    def setTitlePos(self,mode:str="TitleCenter"):
        self.title_pos = mode

    # 设置 缩小,放大,关闭 按钮的风格
    def setBtnStyle(self, style: str = "WinStyle"):
        self.zm.setBtnStyle(style)
        self.lm.setBtnStyle(style)
        self.cm.setBtnStyle(style)

    # 设置标题栏高度
    def setTitleHeight(self,h:int):
        self.h = h

    def setParent(self, parent:QWidget) -> None:
        self.__parent = parent
        super().setParent(parent)

        if self.__parent is not None:
            self.move(0,0)
            self.resize(self.__parent.width(),self.h)

    # 绘制标题
    def drawTitleText(self,painter: QPainter):
        # 绘制文字
        f = QFont()
        f.setPointSize(self.title_size)
        painter.setFont(f)

        op = QPen()
        op.setColor(self.title_color)
        painter.setPen(op)

        # 文字
        fs = QFontMetricsF(f)
        fw = int(fs.width(self.title_text))
        fh = int(fs.height())
        if self.title_pos == TitleBar.Title_Center:
            painter.drawText(self.width() // 2 - fw // 2, self.height() // 2 + fh // 4, self.title_text)

        if self.title_pos == TitleBar.Title_Left:
            painter.drawText(10, self.height() // 2 + fh // 4, self.title_text)


    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(painter.Antialiasing | painter.SmoothPixmapTransform | painter.TextAntialiasing)

        self.drawTitleText(painter)

        painter.end()

    # 创建缩小,放大,关闭事件
    def createEvent(self):
        self.zm.clicked.connect(lambda :self.ani("zoom"))
        self.lm.clicked.connect(lambda :self.ani("arge"))
        self.cm.clicked.connect(lambda :self.ani("close"))

    # 缩小,放大,关闭 动画
    def ani(self,action:str):
        animation = QPropertyAnimation(self.__parent)
        animation.setPropertyName(b"size")
        animation.setTargetObject(self.__parent)
        animation.setDuration(300)

        if action == "zoom":
            self.__parent.showMinimized()
        elif action == "arge":
            self.__parent.move(0,0)
            animation.setStartValue(self.__parent.size())
            animation.setEndValue(QApplication.desktop().size())
            animation.start()
        elif action == "close":
            self.__parent.close()

    # 更新标题栏大小
    def updateTitleSize(self) -> None:
        self.move(0, 0)
        self.resize(self.__parent.width(), self.h)

        # 自动计算 缩小,放大,关闭 的位置
        btn_w_interval = 15 # 按钮直接的间隔
        # 按钮占据的总宽度
        btn_occupied_width = self.zm.width()+self.lm.width()+self.cm.width()+btn_w_interval*3
        occ_w = self.width()-btn_occupied_width
        self.zm.move(occ_w,5)
        occ_w = occ_w+self.zm.width()+btn_w_interval
        self.lm.move(occ_w,5)
        occ_w  = occ_w+self.lm.width()+btn_w_interval
        self.cm.move(occ_w,5)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ZoomButton()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())