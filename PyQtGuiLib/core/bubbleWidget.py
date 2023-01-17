from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QWidget,
    QPainter,
    QPainterPath,
    QPaintEvent,
    QPolygonF,
    QRectF,
    QFont,
    QColor,
    QPointF,
    Signal,
    QBrush,
    QSize,
    textSize,
    QPainterPath,
    QRect,
    QPen,
    qt,
    QStyleOption,
    QStyle,
    QFrame,
)
from PyQt5.QtCore import pyqtProperty

class BubbleWidget(QWidget):

    # 方向
    Top = "top"
    Down = "Down"
    Left = "Left"
    Right = "Right"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setMinimumWidth(0)

        self.setAttribute(qt.WA_StyledBackground, True)
        self.setWindowFlags(qt.FramelessWindowHint | qt.Widget)


        # 箭头高度(三角形)
        self.arrows_h = 20

        # 外边距
        self.margin = 3

        # 半径
        self.radius = 3

        # 文字
        self.text = "气泡窗口"
        self.text_size = 10

        # 三角形颜色,矩形颜色
        self.triangle_color = QColor(152, 167, 255)
        self.rect_color = QColor(152, 167, 255)

        self.direction = BubbleWidget.Right

    def set_rect_color(self,v:QColor):
        self.rect_color = v

    def get_rect_color(self)->QColor:
        return self.rect_color

    # 设计气泡箭头方向
    def setDirection(self,d):
        self.direction = d

    # 控件追踪
    def setTrack(self, widget: QWidget, offset: int = 0):
        pass

    def drawBubble(self,painter:QPainter,ppath:QPainterPath):
        # 矩形高度
        rect_h = self.height() - self.arrows_h
        rect_w = self.width() - self.arrows_h
        # 画三角
        line_w = 20  # 线宽
        lien_x = self.width() // 2 - line_w // 2  # 线的位置-水平
        line_y = self.height()//2  # 线的位置-垂直

        # 绘制文字
        f = QFont()
        f.setPointSize(self.text_size)
        painter.setFont(f)
        # 文字大小
        fs = textSize(f, self.text)
        fw = fs.width()
        fh = fs.height()

        # 画刷
        bru = QBrush(self.rect_color)
        painter.setBrush(bru)

        # 画笔
        painter.setPen(qt.NoPen)

        if self.direction == BubbleWidget.Top:
            # 画三角
            ploys = [QPointF(lien_x,self.arrows_h,),QPointF(lien_x+line_w//2,1),
                     QPointF(lien_x+line_w,self.arrows_h)
                     ]
            # 画矩形
            rect = QRect(self.margin,self.arrows_h+self.margin,self.width()-self.margin*2,rect_h-self.margin*2)
            # 文字位置
            x = self.width() // 2 - fw // 2
            y = rect_h//2 + fh//2+self.arrows_h
        elif self.direction == BubbleWidget.Left:
            # 画三角
            ploys = [QPointF(1,line_y),QPointF(self.arrows_h,line_y-line_w//2),
                     QPointF(self.arrows_h,line_y+line_w//2)
            ]
            rect = QRect(self.arrows_h+self.margin,self.margin,rect_w-self.margin*2,self.height()-self.margin*2)
            # 文字位置
            x = self.width()//2-self.arrows_h
            y = self.height()//2 + fh//2
        elif self.direction == BubbleWidget.Right:
            # 画三角
            ploys =[QPointF(rect_w,line_y-line_w//2),QPointF(rect_w+self.arrows_h,line_y),
                    QPointF(rect_w,line_y+line_w//2)
            ]
            rect = QRect(self.margin,self.margin,rect_w-self.margin*2,self.height()-self.margin*2)
            # 文字位置
            x = (self.width()-self.arrows_h)//2 - fw//2
            y = self.height()//2 + fh//2
        else: # Down
            rect = QRect(self.margin,self.margin,self.width()-self.margin*2,rect_h-self.margin*2)
            # 画三角
            ploys =[QPointF(lien_x,rect_h),
                    QPointF(lien_x+line_w//2,rect_h+self.arrows_h),
                    QPointF(lien_x+line_w,rect_h)]
            # 文字位置
            x = self.width() // 2 - fw//2
            y = rect_h // 2 + fh//2
        # ----
        painter.drawRoundedRect(rect, self.radius, self.radius)
        ppath.addPolygon(QPolygonF(ploys))
        painter.fillPath(ppath, self.triangle_color)

        op = QPen()
        op.setColor(QColor(255, 255, 255))
        painter.setPen(op)
        painter.drawText(x,y, self.text)

    def paintEvent(self, e:QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)

        ppath = QPainterPath()

        # 绘制气泡
        self.drawBubble(painter,ppath)



        painter.end()

    rectColor = pyqtProperty(QColor,fset=set_rect_color,fget=get_rect_color)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = BubbleWidget()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())