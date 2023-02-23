
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
    QPaintEvent
)

class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super(Test, self).__init__(*args,**kwargs)
        self.resize(800,600)

        self.setAttribute(qt.WA_TranslucentBackground,True)
        self.setWindowFlags(qt.FramelessWindowHint | qt.Widget)

        self.spring = 5

    def drawBorder(self,painter:QPainter,rect:QRect):
        rect.setWidth(rect.width()-1)
        rect.setHeight(rect.height()-1)

        op = QPen()
        op.setColor(QColor(0, 225, 0))
        op.setWidth(self.spring*2)
        painter.setPen(op)
        painter.drawRect(rect)

        painter.setPen(qt.NoPen)

    def paintEvent(self, e:QPaintEvent) -> None:
        painter = QPainter(self)

        rect = e.rect()
        self.drawBorder(painter,rect)
        print(rect)

        rect.setRect(rect.x()+self.spring,
                     rect.y()+self.spring,
                     rect.width()-self.spring*2,
                     rect.height()-self.spring*2)

        painter.setBrush(QColor(255,0,100))
        painter.drawRect(rect)
        print(rect)

        painter.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())