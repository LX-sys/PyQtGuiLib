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
    QMouseEvent
)

import time
from PyQt5.QtWidgets import QSplashScreen,QDialog,QProxyStyle
from PyQt5.QtCore import QThread,QRunnable,QThreadPool
from PyQt5.QtGui import QFontMetrics,QFocusEvent

# QSplashScreen
'''
    测试用例的标准模板,该代码用于复制
'''
from PyQtGuiLib.core.resolver import dumpStructure

class myBtn(QPushButton):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(150,50)

class Line(QLineEdit):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(150,50)
    
    # def focusInEvent(self, a0: QtGui.QFocusEvent) -> None:
    #     super(Line, self).focusInEvent()

class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

        self.btn = myBtn(self)
        self.btn.move(20,20)
        self.btn.setText("Test")
        self.btn.mousePressEvent = self.patch

        self.line = Line(self)
        self.line.move(50,100)
        self.line.focusInEvent=self.linePatch

    def patch(self,e:QMouseEvent):
        print("e:",e.buttons())
        super(myBtn,self.btn).mousePressEvent(e)
    
    def linePatch(self,e:QFocusEvent):
        # 带光标的
        super(Line, self.line).focusInEvent(e)
        # 不带光标的
        # super(QLineEdit, self.line).focusInEvent(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())