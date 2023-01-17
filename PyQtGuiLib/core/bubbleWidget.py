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
    qt
)

class BubbleWidget(QWidget):

    # 方向
    Top = "top"
    Down = "Down"
    Left = "Left"
    Right = "Right"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        # 箭头高度
        self.arrows_h = 20

        # 外边距
        self.margin = 3

        # 半径
        self.radius = 3

        # 文字
        self.text = "气泡窗口"

        # 三角形颜色,矩形颜色
        self.triangle_color = QColor(152, 167, 255)
        self.rect_color = QColor(152, 167, 255)

        self.direction = BubbleWidget.Right

    # 设计气泡箭头方向
    def setDirection(self,d):
        self.direction = d

    def drawBubble(self,painter:QPainter,ppath:QPainterPath):
        # 矩形高度
        rect_h = self.height() - self.arrows_h
        rect_w = self.width() - self.arrows_h
        # 画三角
        line_w = 20  # 线宽
        triangle_h = self.arrows_h  # 三角形高度
        lien_x = self.width() // 2 - line_w // 2  # 线的位置-水平
        line_y = self.height()//2 - line_w//2  # 线的位置-垂直


        # 绘制文字
        f = QFont()
        f.setPointSize(10)
        painter.setFont(f)
        # 文字大小
        fs = textSize(f, self.text)
        fw = fs.width()
        fh = fs.height()
        test_fh = 0 # 文字垂直居中
        test_fw = 0 # 文字水平居中

        # 画刷
        bru = QBrush(self.rect_color)
        painter.setBrush(bru)

        # 画笔
        painter.setPen(qt.NoPen)

        if self.direction == BubbleWidget.Top:
            # 画三角
            ploys = [QPointF(lien_x,triangle_h,),QPointF(lien_x+line_w//2,1),
                     QPointF(lien_x+line_w,triangle_h)
                     ]
            # 画矩形
            rect = QRect(self.margin,triangle_h+self.margin,self.width()-self.margin*2,rect_h-self.margin*2)

            test_fh = fh//2+triangle_h
        elif self.direction == BubbleWidget.Left:
            # 画三角
            ploys = [QPointF(1,line_y),QPointF(triangle_h,line_y-line_w//2),
                     QPointF(triangle_h,line_y+line_w//2)
            ]
            rect = QRect(triangle_h+self.margin,self.margin,rect_w,self.height()-self.margin*2)
            test_fh = fh+self.margin
        elif self.direction == BubbleWidget.Right:
            # 画三角
            ploys =[QPointF(rect_w,line_y-line_w//2),QPointF(rect_w+triangle_h,line_y),
                    QPointF(rect_w,line_y+line_w//2)
            ]
            rect = QRect(self.margin,self.margin,rect_w-self.margin*2,self.height()-self.margin)
            test_fh = fh + self.margin
        else: # Down
            rect = QRect(self.margin,self.margin,self.width()-self.margin*2,rect_h-self.margin*2)
            # 画三角
            ploys =[QPointF(lien_x,rect_h),
                    QPointF(lien_x+line_w//2,rect_h+triangle_h),
                    QPointF(lien_x+line_w,rect_h)]
            test_fh = fh // 2
        # ----

        painter.drawRoundedRect(rect, self.radius, self.radius)
        ppath.addPolygon(QPolygonF(ploys))
        painter.fillPath(ppath, self.triangle_color)


        op = QPen()
        op.setColor(QColor(255, 255, 255))
        painter.setPen(op)
        painter.drawText(self.width() // 2 - fw // 2, rect_h // 2 + test_fh, self.text)

    def paintEvent(self, e:QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)

        ppath = QPainterPath()

        # 绘制气泡
        self.drawBubble(painter,ppath)

        painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = BubbleWidget()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())