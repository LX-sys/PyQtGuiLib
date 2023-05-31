# -*- coding:utf-8 -*-
# @time:2023/5/269:53
# @author:LX
# @file:test_PaletteTools.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QColor,
    QVBoxLayout,
    QLabel,
    QPushButton
)

from PyQtGuiLib.core import PaletteTools


'''

'''

class Test(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(500, 300)

        self.vlay = QVBoxLayout(self)

        self.view = QLabel()
        self.view.setMinimumHeight(100)
        self.view.move(10, 10)

        self.btn = QPushButton()
        self.btn.setText("打开调色板")
        self.btn.setFixedHeight(50)

        self.vlay.addWidget(self.view)
        self.vlay.addWidget(self.btn)

        # 作为子窗口嵌入
        # self.ptools = PaletteTools()
        # self.vlay.addWidget(self.ptools)
        # self.ptools.setEnableRealTimeSignal(True)
        # self.ptools.clickSolidColor.connect(lambda c: self.view.setStyleSheet("background-color:" + c))
        # self.ptools.clickStrColor.connect(lambda c: self.view.setStyleSheet("background-color:" + c))

        self.btn.clicked.connect(self.updateColor)

    def updateColor(self):
        if not hasattr(self, "ptools"):
            self.ptools = PaletteTools()
            # 激活颜色实时跟踪
            self.ptools.setEnableRealTimeSignal(True)
            self.ptools.clickSolidColor.connect(lambda c: self.view.setStyleSheet("background-color:" + c))
            self.ptools.clickStrColor.connect(lambda c: self.view.setStyleSheet("background-color:" + c))
        self.ptools.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
