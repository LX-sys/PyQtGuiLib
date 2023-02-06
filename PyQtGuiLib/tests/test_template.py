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
)

import time
from PyQt5.QtWidgets import QSplashScreen,QDialog,QProxyStyle
from PyQt5.QtCore import QThread,QRunnable,QThreadPool

# QSplashScreen
'''
    测试用例的标准模板,该代码用于复制
'''
from PyQtGuiLib.core.resolver import dumpStructure


class SubWidget(QWidget):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.setContentsMargins(0,0,0,0)
        self.setAttribute(Qt.WA_Hover)
#         self.setStyleSheet('''
# background-color: rgba(158, 255, 0, 255);
# border:none;
#         ''')



class Test(QMainWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

        self.btn = QPushButton("打开窗口",self)
        self.btn.move(30,30)
        self.btn.clicked.connect(self.openShow)
        self.btn.blockSignals(False)

        self.subWin = SubWidget()
        self.subWin.resize(300,300)

    def openShow(self):
        self.subWin.show()




if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())