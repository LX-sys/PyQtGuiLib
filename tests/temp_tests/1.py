import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QBitmap, QPainter, QColor
from PyQt5.QtCore import Qt,QSize

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        # 创建一个圆形掩码
        self.mask = QBitmap(self.size())
        self.mask.fill(Qt.black)



    def paintEvent(self, e) -> None:
        painter = QPainter(self.mask)
        painter.setBrush(QColor(Qt.white))
        painter.drawEllipse(-25, -25, 50, 50)
        painter.setPen(Qt.green)
        painter.setBrush(QColor(Qt.green))
        painter.drawRect(0,0,30,30)
        self.setMask(self.mask)

        painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    app.exec_()
