# -*- coding:utf-8 -*-
# @time:2022/12/1019:30
# @author:LX
# @file:__init__.py.py
# @software:PyCharm
from PyQt5.QtCore import QPropertyAnimation, QRect
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QApplication
import sys

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(QRect(100, 100, 200, 200))
        self.setStyleSheet("background-color: red;")

        self.animation = QPropertyAnimation(self, b"backgroundColor")
        self.animation.setDuration(3000)
        self.animation.setStartValue(QColor(255, 0, 0))
        self.animation.setEndValue(QColor(0, 255, 0))
        self.animation.valueChanged.connect(self.cc)
        self.animation.start()

    def cc(self, color):
        print(color.name())
        self.setStyleSheet(f"background-color: {color.name()};")

    # def backgroundColor(self):
    #     print(self.backgroundRole())
    #     return self.palette().color(self.backgroundRole())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())
