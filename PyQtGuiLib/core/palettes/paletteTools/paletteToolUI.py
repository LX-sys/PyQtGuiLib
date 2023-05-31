# -*- coding:utf-8 -*-
# @time:2023/5/2715:31
# @author:LX
# @file:paletteToolUI.py
# @software:PyCharm
from PyQtGuiLib.header import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    Signal,
    QLabel,
    QLineEdit,
    QPainter,
    QSpacerItem,
    QSizePolicy,
    Qt,
    QFormLayout,
    QStackedWidget,
    QColor,
    qt,
    QTimer,
    QCursor,
    QPoint
)

from PyQtGuiLib.core.switchButtons.swButton import SwitchButton
from PyQtGuiLib.styles.styleAnalysis import QssStyleAnalysis
from PyQtGuiLib.core.slideShow import SlideShow
from PyQtGuiLib.styles.superPainter.superPainter import SuperPainter, VirtualObject


Handle_pure = "pure"
Handle_Linear = "linear"
Handle_Radial = "radial"
Handle_Conical = "conical"

G_Mode_Pad = "pad"
G_Mode_Repeat = "repeat"
G_Mode_Reflect = "reflect"


class MaskWidget(QWidget):
    clickColor = Signal(QColor)

    def __init__(self):
        super().__init__()
        self.size = 150
        self.half_size = self.size//2

        self.resize(self.size, self.size)
        self.setWindowFlags(qt.FramelessWindowHint)
        self.setWindowOpacity(0.01)

        self.setCursor(Qt.CrossCursor)

        self.timer = QTimer()
        self.timer.timeout.connect(self.updatePos)

    def updatePos(self):
        self.move(QCursor.pos()-QPoint(self.half_size, self.half_size))
        screen = QApplication.primaryScreen()
        if screen is not None:
            pos = QCursor.pos()
            pixmap = screen.grabWindow(0, pos.x(), pos.y(), 1, 1)
            color = pixmap.toImage().pixelColor(0, 0)
            self.clickColor.emit(color)

    def show(self) -> None:
        self.timer.start(15)
        super().show()

    def mousePressEvent(self, e) -> None:
        self.timer.stop()
        self.close()
        super().mousePressEvent(e)


# 纯色,渐变,径向,辐射(角度)渐变 的 切换 部件类
class StateColorActionBarUI(QWidget):
    clicked = Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.core_hlay = QHBoxLayout(self)
        self.core_hlay.setAlignment(Qt.AlignLeft)

        self.pure_color = QPushButton()
        self.linear_color_btn = QPushButton()
        self.radial_color_btn = QPushButton()
        self.conical_color_btn = QPushButton()

        self.pure_color.setToolTip("纯色")
        self.linear_color_btn.setToolTip("线性渐变")
        self.radial_color_btn.setToolTip("径向渐变")
        self.conical_color_btn.setToolTip("角度渐变")

        for btn in [self.pure_color, self.linear_color_btn, self.radial_color_btn, self.conical_color_btn]:
            btn.setFixedSize(24, 24)
            self.core_hlay.addWidget(btn)

        self.pure_color.setObjectName("pure_color")
        self.linear_color_btn.setObjectName("linear_color")
        self.radial_color_btn.setObjectName("radial_color")
        self.conical_color_btn.setObjectName("conical_color")

        self.defaultStyle()

        self.pure_color.clicked.connect(lambda :self.__click_event(Handle_pure))
        self.linear_color_btn.clicked.connect(lambda :self.__click_event(Handle_Linear))
        self.radial_color_btn.clicked.connect(lambda :self.__click_event(Handle_Radial))
        self.conical_color_btn.clicked.connect(lambda :self.__click_event(Handle_Conical))

    def __click_event(self,state):
        for name in [Handle_pure,Handle_Linear,Handle_Radial,Handle_Conical]:
            if state == name:
                self.qss.selector("#{}_color".format(name)).updateAttr("border","2px solid white")
            else:
                self.qss.selector("#{}_color".format(name)).updateAttr("border","2px solid black")
        self.clicked.emit(state)

    def defaultStyle(self):
        self.qss = QssStyleAnalysis(self)
        self.qss.setQSS('''
#pure_color,#linear_color,#radial_color,#conical_color{
border-radius:12px;
border:2px solid black;
}
#pure_color:hover,#linear_color:hover,#radial_color:hover,#conical_color:hover{
border:3px solid white;
}
#pure_color:pressed,#linear_color:pressed,#radial_color:pressed,#conical_color:pressed{
border:2px solid black;
}
#pure_color{
border:2px solid white;
background-color: rgb(255, 170, 0);
}
#linear_color{
background-color:qlineargradient(spread:pad,x1:0.002,y1:0.457,x2:0.957,y2:0.463,stop:0.49148936170212765 rgba(217, 155, 9, 255),stop:0.5893617021276596 rgba(173, 166, 147, 255));
}
#radial_color{
background-color:qradialgradient(spread:pad,cx:0.436,cy:0.483,radius:0.462,fx:0.47,fy:0.533,stop:0.49148936170212765 rgba(217, 155, 9, 255),stop:0.5893617021276596 rgba(173, 166, 147, 255));
}
#conical_color{
background-color:qconicalgradient(cx:0.448, cy:0.42, angle:120 stop:0.49148936170212765 rgba(217, 155, 9, 255),stop:0.5893617021276596 rgba(173, 166, 147, 255));
}
        ''')

    def paintEvent(self, e) -> None:
        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing,True)

        painter.end()


# 切换渐变模式UI 部件类
class GradientModeActionBarUI(QWidget):
    clicked = Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.core_hlay = QHBoxLayout(self)
        self.core_hlay.setAlignment(Qt.AlignLeft)

        self.pad_btn = QPushButton()
        self.repeat_btn = QPushButton()
        self.reflect_btn = QPushButton()

        for btn in [self.pad_btn,self.repeat_btn,self.reflect_btn]:
            btn.setFixedSize(48,24)
            self.core_hlay.addWidget(btn)

        self.pad_btn.setObjectName("pad_mode")
        self.repeat_btn.setObjectName("repeat_mode")
        self.reflect_btn.setObjectName("reflect_mode")

        self.defaultStyle()

        self.pad_btn.clicked.connect(lambda :self.__click_event(G_Mode_Pad))
        self.repeat_btn.clicked.connect(lambda :self.__click_event(G_Mode_Repeat))
        self.reflect_btn.clicked.connect(lambda :self.__click_event(G_Mode_Reflect))

    def __click_event(self,mode):
        for name in [G_Mode_Pad,G_Mode_Repeat,G_Mode_Reflect]:
            if mode == name:
                self.qss.selector("#{}_mode".format(name)).updateAttr("border","2px solid white")
            else:
                self.qss.selector("#{}_mode".format(name)).updateAttr("border","2px solid black")
        self.clicked.emit(mode)

    def defaultStyle(self):
        self.qss = QssStyleAnalysis(self)
        self.qss.setQSS('''
#pad_mode:hover,#repeat_mode:hover,#reflect_mode:hover{
border:2px solid white;
}
#pad_mode,#repeat_mode,#reflect_mode,#pad_mode:pressed,#repeat_mode:pressed,#reflect_mode:pressed{
border:2px solid back;
border-radius:3px;
}
#pad_mode{
border:2px solid white;
background-color: qlineargradient(spread:pad, x1:0.001, y1:0.471, x2:1, y2:0.482955, stop:0 rgba(232, 200, 97, 255), stop:1 rgba(174, 174, 174, 255));
}
#repeat_mode{
background-color:qlineargradient(spread:repeat, x1:0.33, y1:0.482364, x2:0.63, y2:0.477273, stop:0 rgba(232, 200, 97, 255), stop:1 rgba(174, 174, 174, 255));
}
#reflect_mode{
background-color:qlineargradient(spread:reflect, x1:0.554, y1:0.475, x2:0.63, y2:0.477273, stop:0 rgba(232, 200, 97, 255), stop:1 rgba(174, 174, 174, 255));
}
        
        
        ''')


# 其他部件类
class ItActionBarUI(QWidget):
    switchClicked = Signal(bool)
    strawColored = Signal(QColor)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.core_hlay = QHBoxLayout(self)
        self.core_hlay.setAlignment(Qt.AlignLeft)

        # 纯色预览方块
        self.color_view = QLabel()
        self.color_view.setFixedSize(24,24)
        # 吸管功能按钮
        self.straw_btn = QPushButton()
        self.straw_btn.setText("吸")
        self.straw_btn.setToolTip("颜色吸管")
        self.straw_btn.setFixedSize(24, 24)
        # 句柄开关按钮
        self.hand_btn = SwitchButton()
        self.hand_btn.setToolTip("渐变句柄 显示/隐藏 开关")
        self.hand_btn.setShape(SwitchButton.Shape_Square)
        self.hand_btn.clicked.connect(self.switchClicked.emit)
        self.hand_btn.setFixedSize(50, 24)
        # 六十进制颜色显示
        self.hex_btn = QPushButton()
        self.hex_btn.setToolTip("点击可以复制")
        self.hex_btn.setFixedSize(65, 24)
        self.hex_btn.setText("#00ff00")

        self.color_view.setObjectName("color_view")
        self.straw_btn.setObjectName("straw_btn")
        self.hand_btn.setObjectName("hand_btn")
        self.hex_btn.setObjectName("hex_btn")

        self.core_hlay.addWidget(self.color_view)
        self.core_hlay.addWidget(self.straw_btn)
        self.core_hlay.addWidget(self.hand_btn)
        self.core_hlay.addWidget(self.hex_btn)

        self.straw_btn.clicked.connect(self.straw)

        self.defaultStyle()

        self.myEvent()

    # 复制颜色到鼠标
    def copyColorButton(self)->str:
        copy_color = QApplication.clipboard()
        copy_color.setText(self.hex_btn.text())
        # 缺少通知动画
        # .....

    # 吸管功能
    def straw(self):
        if not hasattr(self,"straw_widget"):
            self.straw_widget = MaskWidget()
            self.straw_widget.clickColor.connect(self.strawColored.emit)
            self.straw_widget.clickColor.connect(self.updateHexView)
        self.straw_widget.show()

    def defaultStyle(self):
        self.setStyleSheet('''
#color_view{
border-radius:2px;
background-color: rgb(88, 142, 128);
}
#straw_btn{
font: 10pt "等线";
background-color: rgb(20, 134, 79);
color: rgb(232, 232, 232);
border:1px solid rgb(85, 170, 127);
border-radius:2px;
}
#straw_btn:pressed{
background-color:rgb(14, 95, 56)
}
#straw_btn:hover{
border-color:white;
}
#hex_btn:hover{
font-size:11pt;
}
#hex_btn,#hex_btn:pressed{
border:none;
color:white;
border-radius:2px;
border-bottom-left-radius:2px;
background-color: rgb(20, 134, 79);
font: 10pt "等线";
}
        ''')

    def updateViewLabel(self,color):
        self.color_view.setStyleSheet('''
        background-color:rgba({},{},{},{});
        '''.format(*color.getRgb()))

    def updateHexColor(self,color):
        self.hex_btn.setText(color.name())

    def updateHexView(self,color):
        self.updateViewLabel(color)
        self.updateHexColor(color)

    def myEvent(self):
        self.hex_btn.clicked.connect(self.copyColorButton)


# -----------------------------

# 纯色的操作台
class PureColorOperationUI(QWidget):
    clickColor = Signal()

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.vlay = QVBoxLayout(self)
        self.vlay.setAlignment(Qt.AlignTop)

        self.labels = [QLabel() for _ in range(4)]
        self.lines = [QLineEdit() for _ in range(4)]

        for i,text in enumerate(["红(R)","绿(G)","蓝(B)","透(A)"]):
            self.labels[i].setText(text)
            self.lines[i].setText("255")

        self.flay = QFormLayout()
        self.flay.setSpacing(3)
        for i in range(4):
            self.flay.addRow(self.labels[i],self.lines[i])
            self.lines[i].setReadOnly(True)

        self.colorButton = QPushButton("获取颜色")
        self.colorButton.setFixedSize(90, 30)
        self.colorButton.setObjectName("colorButton")
        self.flay.setWidget(self.flay.rowCount(), QFormLayout.SpanningRole, self.colorButton)

        self.vlay.addLayout(self.flay)

        self.colorButton.clicked.connect(self.clickColor.emit)

        self.defaultStyle()

    def updateRGB(self,color):
        self.lines[0].setText(str(color.red()))
        self.lines[1].setText(str(color.green()))
        self.lines[2].setText(str(color.blue()))

    def updateAlpha(self, v:int):
        self.lines[3].setText(str(v))

    def defaultStyle(self):
        self.setStyleSheet('''
QLabel{
color: rgb(108, 210, 171);
font: 11pt "等线";
}
QLineEdit{
border:none;
background-color: rgba(23, 154, 93,100);
color: rgb(209, 209, 209);
}
#colorButton:hover{
background-color: rgb(74, 120, 108);
}
#colorButton,#colorButton:pressed{
border-radius:3px;
background-color: rgb(88, 142, 128);
color: rgb(255, 255, 255);
font: 11pt "等线";
}
        ''')


# 渐变操作台
class GradientOperationUI(QWidget):
    clickQSS = Signal()

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.vlay = QVBoxLayout(self)
        self.vlay.setAlignment(Qt.AlignTop)

        self.qss = QPushButton()
        self.qss.setObjectName("qss")
        self.qss.setText("获取QSS")
        self.qss.setFixedSize(90,30)

        self.qss.clicked.connect(self.clickQSS.emit)

        self.vlay.addWidget(self.qss)

        self.defaultStyle()

    def defaultStyle(self):
        self.setStyleSheet('''
#qss{
border-radius:3px;
background-color: rgb(88, 142, 128);
color: rgb(255, 255, 255);
font: 11pt "等线";
}
#qss:hover{
background-color: rgb(74, 120, 108);
}
        ''')


class LinearOperationUI(GradientOperationUI):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)


class RadialOperationUI(GradientOperationUI):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)


class ConicalOperationUI(GradientOperationUI):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)


class PaletteToolsUI(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600, 400)

        self.setWindowTitle("Palette")
        self.setObjectName("widget")

        self.core_vlay = QVBoxLayout(self)

        self.createActionBarUI()
        self.createBodyUI()

        self.defaultStyle()

    def createActionBarUI(self):
        self.action_top_hlay = QHBoxLayout()

        # 主要小部件
        self.state_action_bar = StateColorActionBarUI()
        self.gm_action_bar = GradientModeActionBarUI()
        self.action_top_hlay.addWidget(self.state_action_bar)
        self.action_top_hlay.addWidget(self.gm_action_bar)

        # 弹簧 区别左右
        self.__spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.action_top_hlay.addItem(self.__spacer)

        # 其他部件
        self.it_action_bar = ItActionBarUI()
        self.action_top_hlay.addWidget(self.it_action_bar)

        self.core_vlay.addLayout(self.action_top_hlay)

    def createBodyUI(self):
        self.body_hlay = QHBoxLayout()
        self.body_hlay.setSpacing(0)

        # 绘制区域
        self.body_st_widget = SlideShow()
        self.body_st_widget.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.body_st_widget.setButtonsHide(True)

        # 操作区域
        self.body_op_widget = QStackedWidget()
        self.body_op_widget.setFixedWidth(100)

        self.body_hlay.addWidget(self.body_st_widget)
        self.body_hlay.addWidget(self.body_op_widget)
        self.core_vlay.addLayout(self.body_hlay)

    def addColorWidget(self,widget:QWidget):
        self.body_st_widget.addWidget(widget)

    def addOperationWidget(self,widget:QWidget):
        self.body_op_widget.addWidget(widget)

    def setCurrentIndex(self,g_type):
        state_dict = {
            Handle_pure:0,
            Handle_Linear:1,
            Handle_Radial:2,
            Handle_Conical:3
        }
        i = state_dict[g_type]
        self.body_st_widget.setCurrentIndex(i)
        self.body_op_widget.setCurrentIndex(i)

    def myEvent(self):
        pass

    def defaultStyle(self):
        self.setStyleSheet('''
*{
    font-family:"等线";
}
#widget{
    background-color:#0b4a2d;
}
''')
