# -*- coding:utf-8 -*-
# @time:2022/12/2716:00
# @author:LX
# @file:comboBox.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QWidget,
    QThread,
    Signal,
    QLineEdit,
    QInputMethodEvent,
    QKeyEvent,
    QPaintEvent,
    QMouseEvent,
    QPainter,
    QPen,
    QFont,
    QResizeEvent,
    QRect,
    QBrush,
    QColor,
    QScrollArea,
    QVBoxLayout,
    QPushButton,
    QLabel,
    Qt,
    QPropertyAnimation,
    QPoint,
    QSize,
    qt
)


'''
    下拉框
'''


class LineEdit(QLineEdit):

    clicked = Signal() # 点击事件

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.setStyleSheet('''
border:none;
        ''')

        # 图标大小
        self.icon_w, self.icon_h = 12, 12
        # 图标位置靠右的位置,距离边的距离
        self.icon_right_margin = 25
        # 圆角
        self.icon_radius = (6,6)
        self.icon_color = QColor(0, 255, 0)

        # 动画开关
        self.animation_switch = False

        # self.startTimer(100)

    def mousePressEvent(self, e:QMouseEvent) -> None:
        self.clicked.emit()
        self.animation_switch = True
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        super().mouseReleaseEvent(e)

    # 绘制图标
    def drawIcon(self,painter:QPainter):
        parent = self.parent() # 父类对象
        h = self.height()//2-self.icon_h//2
        rect = QRect(parent.width() - self.icon_right_margin, h, self.icon_w,self.icon_h)

        op = QPen()
        op.setColor(self.icon_color)
        bush = QBrush(self.icon_color)

        painter.setPen(op)
        painter.setBrush(bush)

        painter.drawRoundedRect(rect,*self.icon_radius)

    # def timerEvent(self, e) -> None:
    #     self.update()



    def paintEvent(self, e: QPaintEvent) -> None:
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)

        # 绘制图标
        self.drawIcon(painter)

        painter.end()


class ScrollArea(QScrollArea):

    # 风格
    Style_Card = "card"  # 卡片

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.resize(500,500)

        self.setStyleSheet('''
        border:none;
                ''')

        # 风格模式
        self.style_mode = ScrollArea.Style_Card

        self.setWidgetResizable(True)
        self.core_widget = QWidget()
        self.setWidget(self.core_widget)

        # 隐藏滚动条
        self.setHorizontalScrollBarPolicy(qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(qt.ScrollBarAlwaysOff)

        # 所有对象
        self.obj = []

        self.__vlay = QVBoxLayout(self.core_widget)
        self.__vlay.setContentsMargins(3,5,3,5)
        self.__vlay.setSpacing(3)

        self.item_fixed_height = 40

    # 卡片风格颜色
    def styleCrad(self)->str:
        style ='''
background-color: #237eff;
border:1px solid #237eff;
border-radius:5px;
color:#ffffff;
        '''
        return style

    def addWidget(self,widget:QWidget):
        if isinstance(widget,str):
            # text = widget
            widget_ = QLabel(widget)


            widget_.setMinimumHeight(self.item_fixed_height)
            # widget.setAlignment(Qt.AlignCenter)
            if self.style_mode == ScrollArea.Style_Card:
                widget_.setStyleSheet(self.styleCrad())
        self.__vlay.addWidget(widget_)
        self.obj.append(widget_)

    def itemChildWidget(self)->list:
        return self.obj

    def itemCount(self)->int:
        return len(self.obj)


class ComboBox(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.w,self.h = 400,40
        self.resize(self.w,self.h)
        self.raise_()

        self.setStyleSheet('font: 11pt "华文细黑";')

        # 展开区域,大小,位置
        self.EA_w = self.w
        self.EA_h = 200
        self.EA_x = 0
        self.EA_y = self.h
        self.EA_area_max_height = 200 # 展开区域默认的最大高度
        self.old_h = self.h  # 保存旧的高度
        self.EA_state = False # 状态,展开,隐藏

        self.EA_up_margin = 0  # 下拉框与选择区域的距离

        # 单个子项高度
        self.item_height = 40

        # 展开区域的伸缩动画持续时间
        self.EA_stretch_ani_duration_time = 400
        # 点击事件标记
        self.click_flag = True

        # 创建选择区域
        self.createcChooseArea()
        # 创建展开区域
        self.createExpandArea()

        self.test()

    def test(self):
        self.setEAUpMargin(0)
        for i in range(10):
            self.addText("选项{}".format(str(i)))

    def resize(self, *args) -> None:
        if len(args) == 1 and isinstance(args[0],QSize):
            self.w = args[0].width(),args[0].height()
        else:
            self.w,self.h = args[0],args[1]

        super().resize(self.w,self.h)

    # 添加文本
    def addText(self,text:str):
        self.EA_widget.addWidget(text)

    # 创建选择区域
    def createcChooseArea(self):
        self.__choose_area = LineEdit(self)
        self.__choose_area.move(0, 0)
        self.__choose_area.resize(self.w, self.h)
        self.__choose_area.clicked.connect(self.expand_event)

    # 设置下拉框与选择区域的距离
    def setEAUpMargin(self,margin:int):
        self.EA_up_margin = margin

    def setItemHeight(self,h:int):
        self.item_height = h

    # 设置展开区域的伸缩动画持续时间
    def setEAStretchAniDuration(self,msecs:int):
        self.EA_stretch_ani_duration_time = msecs

    # 创建展开区域
    def createExpandArea(self):
        self.EA_widget = ScrollArea(self)
        self.EA_widget.move(self.EA_x,self.EA_y)
        self.EA_widget.resize(self.EA_w,self.EA_h+self.EA_up_margin)

    # 展开事件
    def expand_event(self):
        if self.EA_state is False:
            self.old_h = self.h
            self.click_flag = False
            self.stretchAni()
            self.EA_state = True
        else:
            self.stretchAni()
            self.EA_state = False

    # 伸缩动画
    def stretchAni(self):
        ani_expand = QPropertyAnimation(self)
        ani_expand.setPropertyName(b"size")
        ani_expand.setTargetObject(self)
        ani_expand.setStartValue(self.size())

        if self.EA_state is False:
            # item个数 * 单个大小 = 总高度
            area_height = self.EA_widget.itemCount() * self.item_height
            if area_height > self.EA_area_max_height:
                area_height = self.EA_area_max_height
            ani_expand.setEndValue(QSize(self.width(),self.height()+area_height))
        else:
            ani_expand.setEndValue(QSize(self.__choose_area.width(),self.__choose_area.height()))

        ani_expand.setDuration(self.EA_stretch_ani_duration_time)
        ani_expand.start()

    def resizeEvent(self, e: QResizeEvent) -> None:
        self.w, self.h = e.size().width(),e.size().height()

        if self.click_flag:
            self.__choose_area.resize(self.w, self.h)
        else:
            self.click_flag = False
            self.__choose_area.resize(self.w,self.old_h)

        #
        self.EA_y = self.h
        self.EA_w = self.w
        self.EA_widget.move(self.EA_x, self.old_h+self.EA_up_margin)
        self.EA_widget.resize(self.EA_w,self.h-self.old_h-self.EA_up_margin)
        super().resizeEvent(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ComboBox()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())