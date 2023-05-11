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
    QRect
)

from random import randint

# from PyQtGuiLib.core.palettes.colorHsv import ColorHsv
from PyQtGuiLib.styles.superPainter.superPainter import SuperPainter


class ColorHsv(QFrame):
    def __init__(self):
        super().__init__()
        self.resize(300,50)

        # 游标宽度
        self.cursor_width = 1

        self.suppainter = SuperPainter()

        self.pix = QPixmap(self.size())
        self.pix.fill(qt.transparent)
        self.createHuePixmap()

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
        if 0 <= x and x <= self.width()-self.cursor_width:
            cursor = self.suppainter.virtualObj("cursor")  # 获取虚拟对象
            y = cursor.getVirtualArgs()[1]
            cursor.move(x,y)
            self.update()

            color = self.pix.toImage().pixelColor(x, y)
            print(color.name())
        super().mouseMoveEvent(e)

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
        self.update()
        super().mousePressEvent(e)

    def paintEvent(self, e) -> None:
        self.suppainter.begin(self)
        # 创建出游标,并设置虚拟对象
        self.suppainter.drawPixmap(e.rect(),self.pix)
        self.suppainter.drawRect(0, 0, self.cursor_width, self.height(), openAttr={"color": "#55aa00", "width": 1},
                                 virtualObjectName="cursor")

        self.suppainter.end()


# 颜色板
class ColorBar(QFrame):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("")
        self.setStyleSheet('''
background-color:rgb(40,177,40);
border-radius:8px;
        ''')


# 调色对话框
class PaletteDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("调色板")
        self.resize(500,400)

        self.setUI()

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
        self.hex_line = QLineEdit()
        self.hex_line.setFixedWidth(100)
        self.hex_line.setStyleSheet('''
border:none;
border-bottom:1px solid rgba(15,10,6,255);
        ''')
        self.hex_line.setText("#000000")

        for btn in [self.pure_color_btn,self.line_btn,self.repeat_btn,self.reflect_btn]:
            btn.setFixedSize(24,24)
            self.__top_lay.addWidget(btn,)

        self.__top_lay.addItem(self.__spacer)
        self.__top_lay.addWidget(self.hex_line)

        # 中间层
        self.__middle_lay = QHBoxLayout()
        self.__middle_lay.setContentsMargins(0,0,0,0)
        self.__middle_lay.setSpacing(3)
        self.__m_v_lay = QVBoxLayout()
        self.color_bar= ColorBar()
        self.hsv_widget = QWidget()
        self.hsv_widget.setFixedHeight(50)
        self.__hsv_lay = QVBoxLayout(self.hsv_widget)
        self.hsv = ColorHsv()
        self.hsv.setFixedHeight(15)
        self.splider = QSlider()
        self.splider.setOrientation(Qt.Horizontal)
        self.__hsv_lay.addWidget(self.hsv)
        self.__hsv_lay.addWidget(self.splider)

        self.__m_v_lay.addWidget(self.color_bar)
        self.__m_v_lay.addWidget(self.hsv_widget)

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
            QSpinBox(),QSpinBox(),
            QSpinBox(),QSpinBox()
        ]
        for line in [self.lineedit_r,self.lineedit_g,self.lineedit_b,self.lineedit_a]:
            line.setMaximum(255)
            # line.setEnabled(False)
        self.lineedit_a.setValue(255)
        self.formLayout = QFormLayout()
        self.formLayout.addRow(self.label_r,self.lineedit_r)
        self.formLayout.addRow(self.label_g,self.lineedit_g)
        self.formLayout.addRow(self.label_b,self.lineedit_b)
        self.formLayout.addRow(self.label_a,self.lineedit_a)
        self.colorButton = QPushButton("获取颜色")
        self.formLayout.setWidget(self.formLayout.rowCount(),QFormLayout.SpanningRole,self.colorButton)

        self._m_r_lay.addLayout(self.formLayout)

        self.__middle_lay.addLayout(self.__m_v_lay)
        self.__middle_lay.addWidget(self._m_r_widget)

        self.__lay.addLayout(self.__top_lay)
        self.__lay.addLayout(self.__middle_lay)
        self.setStyleSheet('''
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
        ''')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ColorHsv()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())