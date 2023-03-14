# -*- coding:utf-8 -*-
# @time:2023/3/1418:29
# @author:LX
# @file:customAniTest.py
# @software:PyCharm
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QAbstractAnimation


class MyAnimation(QAbstractAnimation):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.color = QColor(255, 0, 0)
        self.start_value = 0
        self.end_value = 100
        self._duration = 0

    def updateState(self, newState: 'QAbstractAnimation.State', oldState: 'QAbstractAnimation.State') -> None:
        print(newState, oldState)
        super(MyAnimation, self).updateState(newState, oldState)

    def updateCurrentTime(self, currentTime):
        value = self.start_value + (self.end_value - self.start_value) * currentTime / self.duration()
        self.widget.set_value(value)

    def setStartValue(self, value):
        self.start_value = value

    def setEndValue(self, value):
        self.end_value = value

    def setDuration(self, duration):
        self._duration = duration

    def currentValue(self):
        return self.widget.value()

    def state(self):
        pass

    def start(self, policy=QAbstractAnimation.DeleteWhenStopped):
        super().start(policy)
        self.widget.animation_started()

    def stop(self):
        super().stop()
        self.widget.animation_stopped()

    def duration(self) -> int:
        return self._duration


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 400)
        self.value = 0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawRect(0, 0, self.width(), self.height())
        painter.setBrush(QColor(0, 0, 0))
        painter.drawRect(0, 0, int(self.width() * self.value / 100), self.height())

    def set_value(self, value):
        self.value = value
        self.update()

    def animation_started(self):
        pass

    def animation_stopped(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWidget()
    animation = MyAnimation(w)
    animation.setDuration(1000)
    animation.setStartValue(0)
    animation.setEndValue(100)
    animation.start()
    w.show()
    sys.exit(app.exec_())
