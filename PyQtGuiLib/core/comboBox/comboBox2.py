# -*- coding:utf-8 -*-
# @time:2022/12/2912:42
# @author:LX
# @file:comboBox2.py
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
    QMoveEvent,
    QComboBox,
    qt
)

class ScrollArea(QScrollArea):
    # 风格
    Style_Card = "card"  # 卡片

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.resize(500,500)

        self.setAttribute(qt.WA_TranslucentBackground, True)
        self.setWindowFlags(qt.FramelessWindowHint)
        self.setAttribute(qt.WA_DeleteOnClose)

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
            widget.setAlignment(qt.AlignCenter)
            if self.style_mode == ScrollArea.Style_Card:
                widget.setStyleSheet(self.styleCrad())
        self.__vlay.addWidget(widget)
        self.adjustSize()


class LineEdit(QLineEdit):
    clicked = Signal() # 点击事件

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.resize(300,40)
        # 图标大小
        self.icon_w, self.icon_h = 12, 12
        # 图标位置靠右的位置,距离边的距离
        self.icon_right_margin = 25
        # 圆角
        self.icon_radius = (6,6)
        self.icon_color = QColor(0, 255, 0)

        # 动画开关
        self.animation_switch = False

        #
        self.scroll_area = ScrollArea()
        # self.startTimer(100)

    def mousePressEvent(self, e:QMouseEvent) -> None:
        self.clicked.emit()
        self.animation_switch = True
        self.scroll_area.show()
        self.scroll_area.move(self.pos().x(),self.pos().y()+70)
        self.scroll_area.resize(self.width(),200)
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        super().mouseReleaseEvent(e)

    def moveEvent(self, e: QMoveEvent) -> None:
        self.scroll_area.move(e.pos().x(),e.pos().y()+self.height())
        super().moveEvent(e)

    # 绘制图标
    def drawIcon(self,painter:QPainter):
        parent = self # 父类对象
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


    def closeEvent(self, e) -> None:
        self.scroll_area.close()
        super().closeEvent(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = LineEdit()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())