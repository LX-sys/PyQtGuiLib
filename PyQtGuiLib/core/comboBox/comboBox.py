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
    QSize
)


'''
    下拉框
'''


class LineEdit(QLineEdit):

    clicked = Signal() # 点击事件

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

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
        painter.setRenderHints(painter.Antialiasing | painter.SmoothPixmapTransform | painter.TextAntialiasing)

        # 绘制图标
        self.drawIcon(painter)

        painter.end()


class ScrollArea(QScrollArea):

    # 风格
    Style_Card = "card"  # 卡片

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.resize(500,500)

        # 风格模式
        self.style_mode = ScrollArea.Style_Card

        self.__vlay = QVBoxLayout(self)
        self.__vlay.setContentsMargins(0,0,0,0)
        self.__vlay.setSpacing(3)

        self.item_fixed_size = (self.width(),30)

    # 卡片风格颜色
    def styleCrad(self)->str:
        style ='''
background-color: rgb(176, 255, 225);
border:1px solid gray;
border-radius:5px;
        '''
        return style

    def addWidget(self,widget:QWidget):
        if isinstance(widget,str):
            widget = QLabel(widget)
            print(widget)
            widget.setFixedHeight(30)
            widget.setAlignment(Qt.AlignCenter)
            if self.style_mode == ScrollArea.Style_Card:
                widget.setStyleSheet(self.styleCrad())
        self.__vlay.addWidget(widget)
        self.adjustSize()


class ComboBox(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.w,self.h = 400,40
        self.resize(self.w,self.h)

        # 展开区域,大小,位置
        self.EA_w = self.w
        self.EA_h = 200
        self.EA_x = 0
        self.EA_y = self.h
        self.EA_area_height = 300 # 展开区域默认高度
        self.old_h = self.h  # 保存旧的高度
        self.EA_state = False # 状态,展开,隐藏

        self.EA_up_margin = 0  # 下拉框与选择区域的距离

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
        self.addText("12345")
        self.addText("sad")
        self.addText("12czxc345")

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

    # 设置展开区域的伸缩动画持续时间
    def setEAStretchAniDuration(self,msecs:int):
        self.EA_stretch_ani_duration_time = msecs

    # 创建展开区域
    def createExpandArea(self):
        self.EA_widget = ScrollArea(self)
        # self.EA_widget.setStyleSheet("border:1px solid blue;")
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
            ani_expand.setEndValue(QSize(self.width(),self.height()+self.EA_area_height))
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
    
    # def keyPressEvent(self, e: QKeyEvent) -> None:
    #     print(e.key())
    #     if e.key() == 16777219:
    #         self.text = self.text[:-1]
    #     else:
    #         self.text += e.text()
    #     self.update()
    #     super().keyPressEvent(e)

    # def paintEvent(self, e: QPaintEvent) -> None:
    #     painter = QPainter(self)
    #
    #     font = QFont()
    #     font.setPointSize(15)
    #     painter.setFont(font)
    #
    #     painter.drawLine(8,0,8,40)
    #     painter.drawRect(0,0,self.w,50)
    #
    #     painter.drawText(10,25,self.text)
    #
    #     painter.end()
    # def inputMethodEvent(self, e: QInputMethodEvent) -> None:
    #     print(e)
    #     super(ComboBox, self).inputMethodEvent(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ComboBox()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())