
import math

from PyQt5.QtCore import Qt, QRectF, QTimer, pyqtProperty, pyqtSignal, QPointF, QSize
from PyQt5.QtGui import QColor, QPainter, QPen, QPainterPath, QFont,QFontMetrics
from PyQt5.QtWidgets import QWidget

from PyQtGuiLib.header import (
    Qt,
    QSize,
    QColor,
    QPainter,
    QPen,
    QPainterPath,
    QFont,
    QFontMetrics,
    QWidget,
    Signal,
    QRectF,
    QPointF
)

class CircularProgressBar(QWidget):
    """
    环形进度条，中间显示百分比进度
    """
    valueChanged = Signal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._penWidth = 3  # 圆环的宽度
        self._startAngle = 450
        self._endAngle = 90
        self._value = 0  # 当前进度
        self._minimum = 0  # 最小值
        self._maximum = 100  # 最大值
        self._bgColor = QColor(255, 255, 255)  # 背景色
        self._progressColor = QColor(0, 255, 0)  # 进度条颜色
        self._textColor = QColor(0, 0, 0)  # 文字颜色
        self._font = self.font()  # 字体
        self._formatStr = "{:.0f}%"  # 显示格式

        # 动画相关
        self._timer = QTimer(self)
        self._step = 0
        self._numSteps = 100
        self._interval = 30

        self._timer.timeout.connect(self._animate)
        self._timer.setInterval(self._interval)

    def setChunkWidth(self, w: int):
        """设置圆环的宽度"""
        self._penWidth = w
        self.update()

    @pyqtProperty(int)
    def value(self):
        return self._value

    def setValue(self, val):
        if val != self._value:
            val = min(self._maximum, max(self._minimum, val))
            self._value = val
            self.valueChanged.emit(self._value)
            self.update()

    def __setValue(self, val):
        val = min(self._maximum, max(self._minimum, val))
        self.valueChanged.emit(self._value) if val != self._value else None
        self._value = val
        self.update()

    def animate(self, targetValue, duration):
        self._timer.stop()
        self._step = 0
        self._numSteps = duration / self._interval
        self._targetValue = targetValue
        self._stepSize = (self._targetValue - self._value) / self._numSteps
        self._timer.start()

    def _animate(self):
        self._step += 1
        if self._step > self._numSteps:
            self._timer.stop()
            self.setValue(self._targetValue)
        else:
            self.setValue(self._value + self._stepSize)

    def minimum(self):
        return self._minimum

    def setMinimum(self, minVal):
        if minVal != self._minimum:
            self._minimum = minVal
            self.__setValue(self._value)

    def maximum(self):
        return self._maximum

    def setMaximum(self, maxVal):
        if maxVal != self._maximum:
            self._maximum = maxVal
            self.__setValue(self._value)

    def setRange(self, minVal, maxVal):
        if minVal != self._minimum or maxVal != self._maximum:
            self._minimum = minVal
            self._maximum = maxVal
            self.__setValue(self._value)

    def setFormat(self, fmt):
        self._formatStr = fmt

    def setFont(self, font):
        self._font = font

    def setBgColor(self, color):
        self._bgColor = color

    def setProgressColor(self, color):
        self._progressColor = color
        self.update()

    def setTextColor(self, color):
        self._textColor = color

    def paintEvent(self, event):
        outerRadius = min(self.width(), self.height()) / 2 - self._penWidth / 2

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen()
        pen.setWidth(self._penWidth)
        painter.setPen(pen)

        painter.save()
        painter.setBrush(Qt.BrushStyle.NoBrush)
        self._bgColor = QColor(self._bgColor)
        painter.setPen(QPen(self._bgColor, self._penWidth))
        painter.drawEllipse(QRectF(self.width() / 2 - outerRadius, self.height() / 2 - outerRadius,
                            outerRadius * 2, outerRadius * 2))
        painter.restore()

        painter.save()
        self._progressColor = QColor(self._progressColor)
        pen = QPen(self._progressColor, self._penWidth)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        path = QPainterPath()
        angle = self._startAngle + (self._endAngle - self._startAngle) * (self._value - self._minimum) / (
                self._maximum - self._minimum)
        path.arcMoveTo(self.width() / 2 - outerRadius, self.height() / 2 - outerRadius,
                       outerRadius * 2, outerRadius * 2, self._startAngle)
        path.arcTo(self.width() / 2 - outerRadius, self.height() / 2 - outerRadius,
                   outerRadius * 2, outerRadius * 2, self._startAngle, angle - self._startAngle)
        painter.drawPath(path)
        painter.restore()

        painter.save()
        painter.setFont(self._font)

        self._textColor = QColor(self._textColor)
        painter.setBrush(self._textColor)

        painter.setPen(self._textColor)
        textRect = QRectF(0, 0, outerRadius * 2, outerRadius * 2)
        textRect.moveCenter(QPointF(self.width() / 2, self.height() / 2))
        painter.drawText(textRect, Qt.AlignmentFlag.AlignCenter, self._formatStr.format(math.ceil(
            (self._value - self._minimum) / (self._maximum - self._minimum) * 100)))
        painter.restore()

    def sizeHint(self):
        fontMetrics = QFontMetrics(self._font)
        textSize = fontMetrics.size(Qt.TextFlag.TextSingleLine, self._formatStr.format(self._maximum))
        diameter = max(textSize.width(), textSize.height()) + self._penWidth + 20
        return QSize(diameter, diameter)

    def minimumSizeHint(self):
        return QSize(10, 10)

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)

        self.progress1 = CircularProgressBar(self)
        self.progress2 = CircularProgressBar(self)
        self.progress3 = CircularProgressBar(self)

        label1 = QLabel("默认风格:")
        label2 = QLabel("自定义风格:")
        label3 = QLabel("动画:", self)

        self.progress2.setBgColor("#444444")
        self.progress2.setProgressColor("#ff00ff")
        self.progress2.setTextColor("red")
        self.progress2.setFormat("{:.1f} %")
        self.progress2.setFont(self.font())

        self.progress3.setBgColor(QColor(0, 0, 0, 50))
        self.progress3.setProgressColor(QColor(255, 102, 153, 255))
        self.progress3.setFont(QFont("HarmonyOS Sans SC", 20))
        self.progress3.setChunkWidth(20)
        self.progress3.setRange(300, 500)
        self.progress3.setStyleSheet("background-color:transparent")

        label3.move(150, 60)
        self.progress3.setGeometry(100, 100, 150, 150)

        # 设置进度
        self.progress1.setValue(50)
        self.progress2.setValue(75)
        # self.progress3.animate(100, 3000)

        vbox = QVBoxLayout()
        vbox.addWidget(label1)
        vbox.addWidget(self.progress1)
        vbox.addWidget(label2)
        vbox.addWidget(self.progress2)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)

        centralWidget = QWidget()
        centralWidget.setLayout(hbox)
        self.setCentralWidget(centralWidget)

        self._startValue = 300
        self._timer = QTimer(self)
        self._timer.setInterval(200)
        self._timer.timeout.connect(self.setProssValue)

        self.btn = QPushButton("开始", self)
        self.btn.move(125, 300)
        self.btn.clicked.connect(self._timer.start)

    def setProssValue(self):
        self.progress3.setValue(self._startValue)
        self._startValue += 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())