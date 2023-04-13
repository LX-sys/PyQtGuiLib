# -*- coding:utf-8 -*-
# @time:2023/4/1316:32
# @author:LX
# @file:test_CircularProgressBar.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QMainWindow,
    QLabel,
    QColor,
    QFont,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QTimer,
    QPushButton
)

'''
    CircularProgressBar 测试用例
'''

from PyQtGuiLib.core.progressBar import CircularProgressBar


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

    win = MainWindow()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
