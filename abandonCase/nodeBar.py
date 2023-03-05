from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QWidget,
    Signal,
    Qt,
    QFont,
    QColor,
    QPen,
    QPainter,
    QPaintEvent,
    QFontMetricsF,
    QSize,
    QResizeEvent
)


'''
    节点进度条(暂时停止研究)
'''
class NodeBar(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.w,self.h =100, 50
        self.resize(600,50)

    def drawEllipses(self,painter:QPainter,n):
        x = 100
        xx=100
        for i in range(n):
            painter.drawEllipse(x, 0, self.h, self.h)
            x+=self.h+xx

    def paintEvent(self, event:QPaintEvent) -> None:
        painter = QPainter()
        painter.begin(self)

        op = QPen()
        op.setColor(QColor(179, 179, 179))
        painter.setPen(op)
        painter.setBrush(QColor(179, 179, 179))

        painter.drawRoundedRect(2,self.height()//2-self.h//4,self.width()-4,self.h//2,5,5)
        self.drawEllipses(painter,3)
        painter.end()

    def resizeEvent(self, event:QResizeEvent) -> None:
        self.h =event.size().height()
        super().resizeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = NodeBar()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())