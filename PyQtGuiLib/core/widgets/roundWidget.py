from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    qt,
    QApplication,
    QWidget,
    QHBoxLayout,
    QGraphicsOpacityEffect,
    QPushButton,
    QPainter,
    QPaintEvent,
    qt,
    QBrush,
    QPen,
    QColor,
    QPainterPath,
    QRectF,
    QGraphicsDropShadowEffect,
    QLinearGradient
)
from PyQtGuiLib.core.widgets import BorderlessWidget,BorderlessFrame

'''
    圆角窗口
'''

class RoundWidget(BorderlessFrame):

    # 渐变的方向
    G_Hertical = "vertical"
    G_Horizontal = "horizontal"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800,600)

        self.setAttribute(qt.WA_TranslucentBackground)

        # 有问题这里
        self.ss = QGraphicsDropShadowEffect(self)
        self.ss.setOffset(0,0)
        self.ss.setBlurRadius(10)
        self.ss.setColor(qt.red)
        self.setGraphicsEffect(self.ss)

        # 圆角半径,注意这个值不要高于 8 否则四个斜角将失去拉伸功能
        self.r = 7

        # 颜色
        self.w_color = QColor(240, 240, 240)
        self.w_b_color = qt.gray

        # 渐变色
        self.is_e_gcolor = False # 是否启用渐变色
        self.w_g_color = [(0.5,QColor(119, 177, 88)),(1,QColor(170, 255, 127))]
        self.w_g_direction = "vertical"  # 渐变方向

        self.border_width = 1

    # 设置圆角半径
    def setRadius(self,r:int):
        self.r = r

    # 窗体颜色
    def setWindowColor(self,color:QColor):
        self.w_color = color

    # 设置是否启用渐变色
    def setEnableGColor(self,b:bool):
        self.is_e_gcolor = b

    # 窗体渐变色
    def setWindowGColor(self,colos:list,direction="horizontal"):
        self.self.w_g = colos
        self.is_e_gcolor = True

    # 窗边框颜色
    def setWindowBorderColor(self,color:QColor):
        self.w_b_color = color

    def paintEvent(self, e: QPaintEvent) -> None:
        painter = QPainter(self)

        if self.w_g_direction == "horizontal":
            gradient = QLinearGradient(0, self.height(), self.width(), self.height()) # 垂直线性渐变
        elif self.w_g_direction == "vertical":
            gradient = QLinearGradient(self.width(), 0, self.width(), self.height())  # 水平线性渐变
        else:
            gradient = QLinearGradient(0, self.height(), self.width(), self.height())  # 线性渐变

        bru = QBrush(self.w_color)
        op = QPen()
        op.setColor(self.w_b_color)
        op.setWidth(3)
        op.setStyle(qt.SolidLine)

        # ====
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform)  # 抗锯齿
        if self.is_e_gcolor:
            for v,c in self.w_g_color:
                gradient.setColorAt(v,c)
            painter.setBrush(gradient)
        else:
            painter.setBrush(bru)
        painter.setPen(op)

        rect = self.rect()
        rect.setLeft(5)
        rect.setTop(self.border_width)
        rect.setWidth(rect.width() - 5)
        rect.setHeight(rect.height() - 5)
        painter.drawRoundedRect(rect, self.r, self.r)

        painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = RoundWidget()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())