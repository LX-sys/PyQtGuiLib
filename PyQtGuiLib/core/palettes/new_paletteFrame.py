# -*- coding:utf-8 -*-
# @time:2023/5/1111:00
# @author:LX
# @file:new_paletteFrame.py
# @software:PyCharm

from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    Qt,
    QSizePolicy,
    QSpacerItem,
    QLineEdit,
    QFrame,
    QSlider,
    QSpinBox,
    QFormLayout,
    QPixmap,
    qt,
    QPainter,
    QLinearGradient,
    QColor,
    QRect,
    Signal,
    QFont,
    QStackedWidget,
    QCursor,
    QTimer,
    desktopSize
)

from random import randint

from PyQtGuiLib.styles.superPainter.superPainter import SuperPainter


class ColorHsv(QFrame):
    rgbaChange = Signal(QColor)
    def __init__(self):
        super().__init__()
        self.resize(300,50)

        self.suppainter = SuperPainter()

    # 创建HSV颜色条
    def createHuePixmap(self):
        painter = QPainter(self.pix)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform)  # 抗锯齿
        gradient = QLinearGradient(self.width(), 0, 0, 0)

        i = 0.0
        gradient.setColorAt(0, QColor.fromHsvF(0, 1, 1, 1))
        while i < 1.0:
            gradient.setColorAt(i, QColor.fromHsvF(i, 1, 1, 1))
            i += 1.0 / 16.0
        gradient.setColorAt(1, QColor.fromHsvF(0, 1, 1, 1))
        painter.setPen(qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRoundedRect(self.rect(),0,0)

    def mouseMoveEvent(self, e) -> None:
        x = e.pos().x()
        cursor = self.suppainter.virtualObj("cursor")  # 获取虚拟对象
        y = cursor.getVirtualArgs()[1]
        w = cursor.getVirtualArgs()[2]
        if 0 <= x and x <= self.width() - w:
            cursor.move(x,y)
            self.update()
            color = self.pix.toImage().pixelColor(x, y)
            self.rgbaChange.emit(color)
        super().mouseMoveEvent(e)

    def resizeEvent(self, e) -> None:
        self.pix = QPixmap(self.size())
        self.pix.fill(qt.transparent)
        self.createHuePixmap()
        if self.suppainter.isVirtualObj("cursor"):
            height = e.size().height()
            cursor = self.suppainter.virtualObj("cursor")
            old_rect = list(cursor.getVirtualArgs())
            old_rect[-1] = height
            cursor.updateArgs(*old_rect)
        super().resizeEvent(e)

    def setColor(self, color:QColor):
        # 计算颜色在颜色条中的位置
        h, s, v, a = color.getHsv()
        x = h / 360 * self.width()
        y = self.suppainter.virtualObj("cursor").getVirtualArgs()[1]
        self.suppainter.virtualObj("cursor").move(x, y)
        self.update()

    def mousePressEvent(self, e) -> None:
        cursor = self.suppainter.virtualObj("cursor")  # 获取虚拟对象
        y = cursor.getVirtualArgs()[1]
        cursor.move(e.pos().x(), y)
        cursor.updateIndexToArgs(2,4)
        self.update()
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e) -> None:
        cursor = self.suppainter.virtualObj("cursor")
        cursor.updateIndexToArgs(2, 1)
        self.update()
        super().mouseReleaseEvent(e)

    def paintEvent(self, e) -> None:
        self.suppainter.begin(self)
        # 创建出游标,并设置虚拟对象
        self.suppainter.drawPixmap(e.rect(),self.pix)
        self.suppainter.drawRect(0, 0, 1, self.height(), openAttr={"color": "white", "width": 1},
                                 virtualObjectName="cursor")

        self.suppainter.end()


# 遮罩窗口
class MaskWidget(QWidget):
    def __init__(self,timer):
        super().__init__()
        self.setWindowFlags(qt.FramelessWindowHint)
        self.setWindowOpacity(0.01)
        self.__timer = timer
        self.setCursor(Qt.CrossCursor)

    def mousePressEvent(self, e) -> None:
        self.__timer.stop()
        self.close()
        super().mousePressEvent(e)


# 颜色板
class ColorBar(QFrame):
    rgbaChange = Signal(QColor)
    def __init__(self):
        super().__init__()
        self.__bgcolor = QColor(0, 255, 0, 255)

        self.is_half = False

        # 当前位置
        self.__cur_pos = (20,20)

        self.suppainter = SuperPainter()

    def setAlpha(self,a:int):
        self.__bgcolor.setAlpha(a)
        self.colorLayer()

    def setBgColor(self,color:QColor):
        self.__bgcolor = color
        self.colorLayer()

    def bgColor(self) -> QColor:
        return self.__bgcolor

    # 灰色图层
    def grayLayer(self):
        self.gray_pix = QPixmap(self.size())
        self.gray_pix.fill(qt.transparent)
        self.createGrayPixmap()

    # 彩色图层
    def colorLayer(self):
        self.pix = QPixmap(self.size())
        self.pix.fill(qt.transparent)
        self.createPixmap()

    def createGrayPixmap(self):
        painter = QPainter(self.gray_pix)
        painter.setRenderHints(qt.Antialiasing)

        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(0, 0, 0, 0))
        gradient.setColorAt(1, QColor("#000"))
        painter.setPen(qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRect(self.rect())

    def createPixmap(self):
        painter = QPainter(self.pix)
        painter.setRenderHints(qt.Antialiasing)

        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor("#fff"))

        gradient.setColorAt(1, self.bgColor())

        painter.setPen(qt.NoPen)
        painter.setBrush(gradient)

        painter.drawRect(self.rect())

    def __updateCursorPos(self,pos):
        cursor = self.suppainter.virtualObj("cursor")
        x, y = pos.x()-10, pos.y()-10
        self.__cur_pos = (x,y)
        cursor.move(x, y)
        pixmap = self.grab()
        color = pixmap.toImage().pixelColor(pos)
        self.rgbaChange.emit(color)
        if y >= self.height()//2:
            cursor.updateOpenAttr({"color":"white","w":2})
        else:
            cursor.updateOpenAttr({"color": "black", "w": 2})
        self.update()

    def mouseMoveEvent(self, e):
        self.__updateCursorPos(e.pos())
        super().mouseMoveEvent(e)

    def curColor(self)->QColor:
        return self.pix.toImage().pixelColor(*self.__cur_pos)

    def mousePressEvent(self, e):
        cursor = self.suppainter.virtualObj("cursor")
        cursor.updateIndexToArgs(2,20)
        cursor.updateIndexToArgs(3,20)
        cursor.updateIndexToArgs(4,10)
        cursor.updateIndexToArgs(5,10)
        self.__updateCursorPos(e.pos())
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        cursor = self.suppainter.virtualObj("cursor")
        cursor.updateIndexToArgs(2,10)
        cursor.updateIndexToArgs(3,10)
        cursor.updateIndexToArgs(4,5)
        cursor.updateIndexToArgs(5,5)
        self.update()
        super().mouseReleaseEvent(e)

    def paintEvent(self, e) -> None:
        self.suppainter.begin(self)
        self.suppainter.setRenderHints(qt.Antialiasing)
        rect = e.rect()
        self.suppainter.drawPixmap(rect,self.pix)
        self.suppainter.drawPixmap(rect,self.gray_pix)
        self.suppainter.drawRoundedRect(20,20,10,10,5,5,openAttr={"color":"black","w":2},virtualObjectName="cursor")
        self.suppainter.end()

    def resizeEvent(self, e) -> None:
        self.grayLayer()
        self.colorLayer()
        super().resizeEvent(e)


# 线性渐变板
class Line(QFrame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setStyleSheet("border:1px solid yellow;")

        self.suppainter = SuperPainter()

        self.linear = QLinearGradient()

    def paintEvent(self, e):
        self.suppainter.begin(self)


        self.suppainter.end()


# 渐变通用操作台
class ColorOperation(QFrame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setFixedHeight(80)
        self.setStyleSheet("border:1px solid red;")



# 调色对话框
class PaletteDialog(QWidget):
    clickColor = Signal(QColor)
    def __init__(self):
        super().__init__()
        self.setObjectName("widget")
        self.setWindowTitle("调色板")
        self.resize(500,400)

        # 吸管定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateColor)

        self.setUI()
        self.myEvent()

    def setUI(self):
        self.__lay = QVBoxLayout(self)

        self.__top_lay = QHBoxLayout()
        self.__top_lay.setSpacing(20)
        self.pure_color_btn = QPushButton()  # 纯色按钮
        self.line_btn = QPushButton() # 线性渐变按钮
        self.repeat_btn = QPushButton() # 径向渐变按钮
        self.reflect_btn = QPushButton() # 角度渐变按钮
        self.pure_color_btn.setObjectName("pure_color_btn")
        self.line_btn.setObjectName("line_btn")
        self.repeat_btn.setObjectName("repeat_btn")
        self.reflect_btn.setObjectName("reflect_btn")
        self.pure_color_btn.setToolTip("纯色")
        self.line_btn.setToolTip("线性渐变")
        self.repeat_btn.setToolTip("径向渐变")
        self.reflect_btn.setToolTip("角度渐变")

        self.__spacer = QSpacerItem(0,0,QSizePolicy.Expanding,QSizePolicy.Minimum)
        self.demonstration_color_l = QLabel()

        self.demonstration_color_l.setFixedSize(24,24)
        self.color_straw_btn = QPushButton() # 吸管
        self.color_straw_btn.setObjectName("color_straw_btn")
        self.color_straw_btn.setText("吸")
        self.color_straw_btn.setFixedSize(24,24)
        self.hex_line = QLineEdit()
        self.hex_line.setFixedSize(100,24)
        self.hex_line.setText("#00ff00")

        for btn in [self.pure_color_btn,self.line_btn,self.repeat_btn,self.reflect_btn]:
            btn.setFixedSize(24,24)
            self.__top_lay.addWidget(btn,)

        self.__top_lay.addItem(self.__spacer)
        self.__top_lay.addWidget(self.demonstration_color_l)
        self.__top_lay.addWidget(self.color_straw_btn)
        self.__top_lay.addWidget(self.hex_line)

        # 中间层
        self.__middle_lay = QHBoxLayout()
        self.__middle_lay.setContentsMargins(0,0,0,0)
        self.__middle_lay.setSpacing(3)

        # ---

        # 纯色,线性渐变,径向渐变,角度渐变
        self.st = QStackedWidget()
        self.st_pure_color_wideget = QWidget()
        self.st_line_widget = QWidget()
        self.st_repeat_widget = QWidget()
        self.st_reflect_widget = QWidget()
        self.st.addWidget(self.st_pure_color_wideget)
        self.st.addWidget(self.st_line_widget)
        self.st.addWidget(self.st_repeat_widget)
        self.st.addWidget(self.st_reflect_widget)

        self.pureColorWidget()
        self.linearColorWidget()
        # -----


        self._m_r_widget = QWidget()
        self._m_r_lay = QVBoxLayout(self._m_r_widget)
        self._m_r_widget.setFixedWidth(100)

        self.label_r,self.label_g,self.label_b,self.label_a = [
            QLabel("红(R)"),
            QLabel("绿(G)"),
            QLabel("蓝(B)"),
            QLabel("透(A)"),
        ]
        self.lineedit_r, self.lineedit_g, self.lineedit_b, self.lineedit_a = [
            QLineEdit(),QLineEdit(),
            QLineEdit(),QLineEdit()
        ]
        for line in [self.lineedit_r,self.lineedit_g,self.lineedit_b,self.lineedit_a]:
            line.setText("255")
        self.lineedit_a.setText("255")
        self.formLayout = QFormLayout()
        self.formLayout.addRow(self.label_r,self.lineedit_r)
        self.formLayout.addRow(self.label_g,self.lineedit_g)
        self.formLayout.addRow(self.label_b,self.lineedit_b)
        self.formLayout.addRow(self.label_a,self.lineedit_a)
        self.colorButton = QPushButton("获取颜色")
        self.colorButton.setFixedSize(90,30)
        self.colorButton.setObjectName("colorButton")
        self.formLayout.setWidget(self.formLayout.rowCount(),QFormLayout.SpanningRole,self.colorButton)

        self._m_r_lay.addLayout(self.formLayout)


        self.__middle_lay.addWidget(self._m_r_widget)

        self.__lay.addLayout(self.__top_lay)
        self.__lay.addLayout(self.__middle_lay)

        # 初始化演示色块
        self.setDemonstrationColor(self.color_bar.bgColor())
        self.setStyleSheet('''
#widget{
background-color:#0b4a2d;
}
#color_straw_btn{
font: 10pt "等线";
background-color: rgb(20, 134, 79);
color: rgb(232, 232, 232);
border:1px solid rgb(85, 170, 127);
border-radius:2px;
}
#color_straw_btn:pressed{
background-color:rgb(14, 95, 56)
}
#pure_color_btn,#line_btn,#repeat_btn,#reflect_btn{
border-radius:12px;
border:2px solid rgba(0,0,0,255);
}
#pure_color_btn:hover,#line_btn:hover,#repeat_btn:hover,#reflect_btn:hover{
border:3px solid rgba(0,0,0,255);
}
#pure_color_btn:pressed,#line_btn:pressed,#repeat_btn:pressed,#reflect_btn:pressed{
border:2px solid rgba(0,0,0,255);
}
#pure_color_btn{
background-color: rgb(255, 170, 0);
}
#line_btn{
background-color:qlineargradient(spread:pad,x1:0.002,y1:0.457,x2:0.957,y2:0.463,stop:0.49148936170212765 rgba(217, 155, 9, 255),stop:0.5893617021276596 rgba(173, 166, 147, 255));
}
#repeat_btn{
background-color:qradialgradient(spread:pad,cx:0.436,cy:0.483,radius:0.462,fx:0.47,fy:0.533,stop:0.49148936170212765 rgba(217, 155, 9, 255),stop:0.5893617021276596 rgba(173, 166, 147, 255));
}
#reflect_btn{
background-color:qconicalgradient(cx:0.448, cy:0.42, angle:120 stop:0.49148936170212765 rgba(217, 155, 9, 255),stop:0.5893617021276596 rgba(173, 166, 147, 255));
}
QLabel{
color: rgb(108, 210, 171);
font: 11pt "等线";
}
#colorButton{
border-radius:5px;
background-color: rgb(88, 142, 128);
color: rgb(255, 255, 255);
font: 11pt "等线";
}
QLineEdit{
border:none;
background-color: rgba(23, 154, 93,100);
color: rgb(209, 209, 209);
}
        ''')

    def updateColor(self):
        # 实现吸管
        pos = QCursor.pos()
        screen = QApplication.primaryScreen()
        if screen is not None:
            pixmap = screen.grabWindow(0, pos.x(), pos.y(), 1, 1)
            color = pixmap.toImage().pixelColor(0, 0)
            self.setDemonstrationColor(color)
            self.setLabelRGB(color)
            self.hex_line.setText(color.name())

    # 纯色面板
    def pureColorWidget(self):
        self.__m_v_lay = QVBoxLayout(self.st_pure_color_wideget)
        self.color_bar = ColorBar()
        self.hsv_widget = QWidget()
        self.hsv_widget.setFixedHeight(50)
        self.__hsv_lay = QVBoxLayout(self.hsv_widget)
        self.hsv = ColorHsv()
        self.hsv.setFixedHeight(15)
        self.splider = QSlider()
        self.splider.setMinimum(0)
        self.splider.setMaximum(255)
        self.splider.setValue(255)
        self.splider.setOrientation(Qt.Horizontal)
        self.__hsv_lay.addWidget(self.hsv)
        self.__hsv_lay.addWidget(self.splider)

        self.__m_v_lay.addWidget(self.color_bar)
        self.__m_v_lay.addWidget(self.hsv_widget)

        self.__middle_lay.addWidget(self.st)

    # 线性面板
    def linearColorWidget(self):
        self.__line_vlay = QVBoxLayout(self.st_line_widget)
        self.linear = Line()

        self.operation_color  = ColorOperation()

        self.__line_vlay.addWidget(self.linear)
        self.__line_vlay.addWidget(self.operation_color)

    def setLabelRGB(self,c:QColor):
        r,g,b,a = c.getRgb()
        self.lineedit_r.setText(str(r))
        self.lineedit_g.setText(str(g))
        self.lineedit_b.setText(str(b))

    def setDemonstrationColor(self,color:QColor):
        self.demonstration_color_l.setStyleSheet('''
        border-radius:3px;
        background-color:{};
        '''.format(color.name()))

    def __update_color_event(self,c):
        self.setLabelRGB(c)
        self.hex_line.setText(c.name())
        self.setDemonstrationColor(c)
        self.update()

    # 更新色块 rgb 事件
    def __update_rgb_event(self,c:QColor):
        self.color_bar.setBgColor(QColor(c))
        self.setLabelRGB(self.color_bar.curColor())
        self.setDemonstrationColor(self.color_bar.curColor())
        self.update()

    # 更新透明度
    def update_a_event(self,value:int):
        self.color_bar.setAlpha(value)
        self.lineedit_a.setText(str(value))
        self.setDemonstrationColor(self.color_bar.curColor())
        self.update()

    # emit
    def __emit_color_event(self):
        self.clickColor.emit(QColor(self.hex_line.text()))

    def straw_event(self):
        self.temp_w = MaskWidget(self.timer)
        self.temp_w.resize(desktopSize())
        self.temp_w.show()
        self.timer.start(50)

    def myEvent(self):
        self.pure_color_btn.clicked.connect(lambda :self.st.setCurrentIndex(0))
        self.line_btn.clicked.connect(lambda :self.st.setCurrentIndex(1))
        self.repeat_btn.clicked.connect(lambda :self.st.setCurrentIndex(2))
        self.reflect_btn.clicked.connect(lambda :self.st.setCurrentIndex(3))

        self.hsv.rgbaChange.connect(self.__update_rgb_event)
        self.color_bar.rgbaChange.connect(self.__update_color_event)

        self.splider.valueChanged.connect(self.update_a_event)

        self.colorButton.clicked.connect(self.__emit_color_event)

        self.color_straw_btn.clicked.connect(self.straw_event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = PaletteDialog()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())