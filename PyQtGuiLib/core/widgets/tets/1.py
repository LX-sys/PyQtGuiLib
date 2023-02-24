
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    qt,
    Qt,
    QPoint,
    QPainter,
    QColor,
    QRect,
    QBrush,
    QPen,
    QPaintEvent,
    QGraphicsDropShadowEffect
)

class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super(Test, self).__init__(*args,**kwargs)
        self.resize(800,600)

        self.setAttribute(qt.WA_TranslucentBackground,True)
        self.setWindowFlags(qt.FramelessWindowHint | qt.Widget)


        self.spring = 1
        self.radius = 150

    def tupleRadius(self)->tuple:
        return self.radius,self.radius

    def drawBorder(self,painter:QPainter,rect:QRect):
        rect.setWidth(rect.width())
        rect.setHeight(rect.height())

        op = QPen()
        op.setColor(QColor(0, 0, 0))
        op.setWidth(self.spring*2)
        painter.setPen(op)
        # painter.drawRect(rect)
        painter.drawRoundedRect(rect,*self.tupleRadius())

        painter.setPen(qt.NoPen)


    # 绘制背景
    def drawBackground(self,painter:QPainter,rect:QRect):
        rect.setRect(rect.x() + self.spring,
                     rect.y() + self.spring,
                     rect.width() - self.spring * 2,
                     rect.height() - self.spring * 2)

        painter.setBrush(QColor(255, 0, 100))
        # painter.drawRect(rect)
        painter.drawRoundedRect(rect,*self.tupleRadius())

    def paintEvent(self, e:QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)

        rect = e.rect()

        self.drawBorder(painter,rect)
        self.drawBackground(painter,rect)

        painter.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())