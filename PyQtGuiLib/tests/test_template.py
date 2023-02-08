from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    qt,
    QPushButton,
    Qt,
    QPalette,
    QColor,
    QPaintEvent,
    QPainter,
    QBrush,
    QSize,
    QMainWindow,
    QLineEdit,
    desktopCenter,
    QPixmap,
    QLinearGradient,
    QLabel,
    QFont,
    textSize,
    QFontMetricsF,
    Qt
)

import time
from PyQt5.QtWidgets import QSplashScreen,QDialog,QProxyStyle
from PyQt5.QtCore import QThread,QRunnable,QThreadPool
from PyQt5.QtGui import QFontMetrics

# QSplashScreen
'''
    测试用例的标准模板,该代码用于复制
'''
from PyQtGuiLib.core.resolver import dumpStructure


class Test(QMainWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())