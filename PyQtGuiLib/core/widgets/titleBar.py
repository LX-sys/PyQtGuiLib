from PyQtGuiLib.header import (
    PYQT_VERSIONS,
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
    QParallelAnimationGroup,
    QBrush,
    qt,
    QSize,
    QPoint,
    QPixmap,
    QIcon,
    QStyle,
    QStyleOption,
    desktopCenter,
    desktopSize,
    textSize
)

from PyQtGuiLib.core.widgets import BorderlessWidget
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

    def resize(self, *args) -> None:
        if len(args) == 1 and isinstance(args[0],QSize):
            self.w = args[0].width(),args[0].height()
        else:
            self.w,self.h = args[0],args[1]

        super().resize(self.w,self.h)

    # 设置 缩小,放大,关闭 的风格
    def setBtnStyle(self,style:str = "WinStyle"):
        self.btnStyle = style
    
    def isWinStyle(self) -> bool:
        return True if self.btnStyle == ButtonIcon.WinStyle else False

    def isMacStyle(self) -> bool:
        return True if self.btnStyle == ButtonIcon.MacStyle else False

    # 绘制图标,所有子类都必须实现都方法
    def drawIcon(self, painter: QPainter):
        pass

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)

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
            op.setColor(QColor(255, 199, 124))
            painter.setPen(op)
            brush = QBrush(QColor(255, 199, 124))
            painter.setBrush(brush)

            rect = QRect(1, 1, self.width() - self.open_width - 1, self.height() - self.open_width - 1)
            painter.drawRoundedRect(rect, self.w//2,self.h//2)
            op.setColor(QColor(50, 100, 100))
            painter.setPen(op)
            painter.drawLine(5, self.height() // 2, self.width() - 5, self.height() // 2)
            painter.setBrush(qt.NoBrush)


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
            op.setColor(QColor(40, 194, 50))
            painter.setPen(op)
            brush = QBrush(QColor(40, 194, 50))
            painter.setBrush(brush)

            rect = QRect(1, 1, self.width() - self.open_width - 1, self.height() - self.open_width - 1)
            painter.drawRoundedRect(rect, self.w//2,self.h//2)

            brush = QBrush(QColor(0,0,0))
            painter.setBrush(brush)
            op.setColor(QColor(50, 100, 100))
            painter.setPen(op)
            painter.drawEllipse(self.width()//2-5,self.height()//2-5,5,5)
            painter.drawEllipse(self.width()//2+1,self.height()//2+1,5,5)

            painter.setBrush(qt.NoBrush)


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
            op.setColor(QColor(252, 70, 70))
            painter.setPen(op)
            brush = QBrush(QColor(252, 70, 70))
            painter.setBrush(brush)

            rect = QRect(1, 1, self.width() - self.open_width - 1, self.height() - self.open_width - 1)
            painter.drawRoundedRect(rect, self.w//2,self.h//2)

            op.setColor(QColor(50, 100, 100))
            painter.setPen(op)

            painter.drawLine(5, 5, self.width() - 5, self.height() - 5)
            painter.drawLine(self.width() - 5, 5, 5, self.height() - 5)


# 钉住窗口按钮
class PegButton(ButtonIcon):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.is_flag = False

    def drawIcon(self,painter:QPainter):
        op = QPen()
        op.setWidth(1)
        painter.setPen(op)

        if self.isWinStyle():
            rect = QRect(1, 1, self.width() - self.open_width - 1, self.height() - self.open_width - 1)
            rect_c = QRect(3, 3, self.width() - 6, self.height() - 6)
            painter.drawRoundedRect(rect, self.radius,self.radius)
            if self.is_flag:
                bru = QBrush(QColor(84, 120, 186))
                painter.setBrush(bru)
            painter.drawRoundedRect(rect_c, self.radius, self.radius)
        elif self.isMacStyle():
            bru = QBrush(qt.black)
            painter.setBrush(bru)

            rect = QRect(1, 1, self.width() - self.open_width - 1, self.height() - self.open_width - 1)
            rect_c = QRect(3, 3, self.width()  - 6, self.height() -6)
            painter.drawRoundedRect(rect, self.w // 2, self.h // 2)
            if self.is_flag:
                bru = QBrush(QColor(171, 0, 0))
                painter.setBrush(bru)
            painter.drawRoundedRect(rect_c, self.w // 2, self.h // 2)


class TitleBar(BorderlessWidget):

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

        # 样式表生效
        self.setAttribute(qt.WA_StyledBackground,True)
        self.setBorderStyle(qt.NoPen)

        self.__parent = None #  type:QWidget

        if args:
            self.__parent = args[0]

        # 默认半径
        self.setRadius((self.radius()[0],0))

        # 标题位置
        self.title_pos = TitleBar.Title_Left

        # 标题高度
        self.h = 30
        # 标题文本
        self.title_text= "Title"
        self.title_color = QColor(0,0,0)
        self.title_size = 15

        # 图标大小,图标路径
        self.image_size = 30,30
        self.title_icon_path = r""
        self.is_sync_icon = True # 是否同步桌面任务栏的图标

        # 保存窗口在放大之前的位置大小,已经窗口大小状态
        self.old_screen_geometry = QRect(0,0,0,0) # type:QRect
        self.screen_state = False

        # 边距
        self.padding = self.borderWidth()

        # 动画时长
        self.ani_msec = 300  # 毫秒

        if self.__parent is not None:
            self.move(self.padd(),self.padd())
            self.resize(self.__parent.width()-self.padd()*2,self.h)

        # 创建缩小,放大,关闭,钉住 按钮
        self.zm = ZoomButton(self)
        self.lm = LargeButton(self)
        self.cm = CloseButton(self)
        self.peg = PegButton(self)
        self.is_pag = False # 是否钉住
        # 创建缩小,放大,关闭事件
        self.createEvent()

        # 设置标题设置
        self.setTitlePos(TitleBar.Title_Center)
        self.updateTitleSize()  # 更新标题栏位置

    # 边距
    def padd(self)->int:
        return self.padding

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
        self.peg.setBtnStyle(style)

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

        icon_distance = 0

        if self.title_icon_path:
            icon_distance = 30

        # 文字
        fs = textSize(f,self.title_text)
        fw = fs.width()
        fh = fs.height()
        if self.title_pos == TitleBar.Title_Center:
            painter.drawText(self.width() // 2 - fw // 2, self.height() // 2 + fh // 2, self.title_text)

        if self.title_pos == TitleBar.Title_Left:
            if PYQT_VERSIONS in ["PyQt6","PySide6"]: # 这两个版本的文字高度计算是精准的需要-5个像素
                painter.drawText(10+icon_distance, self.height() // 2 + fh // 2-5, self.title_text)
            else:
                painter.drawText(10+icon_distance, self.height() // 2 + fh // 2, self.title_text)

    # 绘制tub
    def drawTitleIcon(self,painter: QPainter):
        f = QFont()
        f.setPointSize(self.title_size)
        fs = textSize(f,self.title_text)
        fw = fs.width()

        pix = QPixmap(self.title_icon_path)
        if self.title_pos == TitleBar.Title_Center:
            painter.drawPixmap(self.width() // 2 - fw // 2-self.image_size[0], self.height() // 2 - self.image_size[1] // 2, *self.image_size,
                               pix)
        if self.title_pos == TitleBar.Title_Left:
            painter.drawPixmap(5, self.height()//2-self.image_size[1]//2, *self.image_size, pix)
        if self.is_sync_icon:
            self.__parent.setWindowIcon(QIcon(self.title_icon_path))

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)
        painter = QPainter(self)

        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)

        self.drawTitleIcon(painter)
        self.drawTitleText(painter)

        # 自动调用
        self.updateTitleSize()
        painter.end()

    # 创建缩小,放大,关闭事件
    def createEvent(self):
        self.zm.clicked.connect(lambda :self.ani("zoom"))
        self.lm.clicked.connect(lambda :self.ani("arge"))
        self.cm.clicked.connect(lambda :self.ani("close"))
        self.peg.clicked.connect(lambda :self.ani("peg"))

    # 设置动画的时长
    def setAniDuration(self,msec:int):
        self.ani_msec = msec

    # 设置图标
    def setTitleIcon(self,path:str,isWindowIcon:bool=True):
        '''

        :param path: 图片路径
        :param isWindowIcon: 是否同步桌面任务栏的图标
        :return:
        '''
        self.title_icon_path = path
        self.is_sync_icon = isWindowIcon

    # 设置是否同步桌面任务栏的图标
    def setSyncWindowIcon(self,b:bool):
        self.is_sync_icon = b

    # 缩小,放大,关闭 动画
    def ani(self,action:str):
        animation = QPropertyAnimation(self.__parent)
        animation.setTargetObject(self.__parent)
        animation.setDuration(self.ani_msec)

        if action == "zoom":
            def _t(parent,size):
                parent.showMinimized()
                parent.setGeometry(size)

            old_geometry = self.__parent.geometry()
            animation.setPropertyName(b"size")
            animation.setStartValue(self.__parent.size())
            animation.setEndValue(QSize(10,10))
            # animation.start()
            animation.finished.connect(lambda :_t(self.__parent,old_geometry))

            # 获取窗口位置的中心点
            center_point = QPoint(self.__parent.x()+self.__parent.width()//2,
                                  self.__parent.y()+self.__parent.height()//2)

            # 移动动画
            animation_move = QPropertyAnimation(self.__parent)
            animation_move.setPropertyName(b"pos")
            animation_move.setTargetObject(self.__parent)
            animation_move.setDuration(self.ani_msec)

            animation_move.setStartValue(self.pos())
            animation_move.setEndValue(center_point)

            # 动画组
            ani_group = QParallelAnimationGroup(self.__parent)
            ani_group.addAnimation(animation_move)
            ani_group.addAnimation(animation)
            ani_group.start()
        elif action == "arge":
            animation.setPropertyName(b"size")

            # 移动动画
            animation_move = QPropertyAnimation(self.__parent)
            animation_move.setPropertyName(b"pos")
            animation_move.setTargetObject(self.__parent)
            animation_move.setDuration(self.ani_msec)

            animation.setStartValue(self.__parent.size())
            animation_move.setStartValue(self.__parent.pos())

            if self.screen_state is False:
                # 保存旧属性和状态
                self.old_screen_geometry = self.__parent.geometry()  # type:QRect

                # 获取的单个屏幕的大小
                animation.setEndValue(desktopSize())
                #
                animation_move.setEndValue(QPoint(0,0))

                self.screen_state = True
            else:
                animation.setEndValue(self.old_screen_geometry.size())
                #
                animation_move.setEndValue(QPoint(self.old_screen_geometry.x(),self.old_screen_geometry.y()))
                self.screen_state = False
            # 动画组
            ani_group = QParallelAnimationGroup(self.__parent)
            ani_group.addAnimation(animation_move)
            ani_group.addAnimation(animation)
            ani_group.start()
        elif action == "close":
            animation.setPropertyName(b"windowOpacity")
            animation.setStartValue(1)
            animation.setEndValue(0)
            animation.start()
            animation.finished.connect(self.__parent.close)
        elif action == "peg":
            if not self.peg.is_flag:
                self.peg.is_flag = True
                self.__parent.windowHandle().setFlags(self.windowFlags() | qt.WindowStaysOnTopHint|
                                                      qt.FramelessWindowHint | qt.Window)
            else:
                self.peg.is_flag = False
                self.__parent.windowHandle().setFlags(self.windowFlags() | qt.Widget|qt.FramelessWindowHint|qt.Window)
            self.__parent.show()
            self.__parent.repaint()
            # self.__parent.update()

    # 更新标题栏大小
    def updateTitleSize(self) -> None:
        self.move(self.padd(), self.padd())
        self.resize(self.__parent.width()-self.padd()*2, self.h+self.padd()*2)

        # 自动计算 缩小,放大,关闭 的位置
        btn_w_interval = 15 # 按钮直接的间隔
        # 按钮占据的总宽度
        btn_occupied_width = self.zm.width()+self.lm.width()+self.cm.width()+btn_w_interval*5
        occ_w = self.width()-btn_occupied_width

        peg_h = self.height() // 2 - self.peg.height() // 2
        zm_h = self.height()//2 - self.zm.height()//2
        lm_h = self.height()//2 - self.lm.height()//2
        cm_h = self.height()//2 - self.cm.height()//2

        self.peg.move(occ_w, peg_h)
        occ_w = occ_w + self.peg.width() + btn_w_interval
        self.zm.move(occ_w,zm_h)
        occ_w = occ_w+self.zm.width()+btn_w_interval
        self.lm.move(occ_w,lm_h)
        occ_w = occ_w+self.lm.width()+btn_w_interval
        self.cm.move(occ_w,cm_h)
