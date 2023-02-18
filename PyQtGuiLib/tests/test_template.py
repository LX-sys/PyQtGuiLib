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
    Qt,
    QMouseEvent,
)

import time
from PyQt5.QtWidgets import QSplashScreen,QDialog,QProxyStyle,QButtonGroup
from PyQt5.QtCore import QThread,QRunnable,QThreadPool
from PyQt5.QtGui import QFontMetrics,QFocusEvent

# QSplashScreen
'''
    测试用例的标准模板,该代码用于复制
'''
from PyQtGuiLib.core.resolver import dumpStructure



class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

        self.btnGroup = QButtonGroup(self)
        self.move(50,50)

        for b in range(1,4):
            btn =QPushButton("test_{}".format(b))
            self.btnGroup.addButton(btn)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())