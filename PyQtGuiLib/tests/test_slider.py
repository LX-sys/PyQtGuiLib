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
    QVBoxLayout,
    QThread
)

from PyQtGuiLib.core import Slider
'''
    测试 滑块
'''
class TestTh(QThread):
    def __init__(self,*args,**kwargs):
        super(TestTh, self).__init__(*args,**kwargs)

    def run(self) -> None:
        while True:
            pass



class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

        self.sl = Slider(self)
        # self.sl.resize(300,40)
        self.sl.setFixedHeight(40)

        self.sl.setHoverIcon(False)
        self.sl.setMaxValue(30000)
        self.sl.move(100,100)
        self.sl.valueChanged.connect(self.test)
        # self.sl.setBuffValue(30)
        self.sl.setStyleSheet('''
        Slider{
qproperty-radius:5;
qproperty-flowColor:rgb(255,0,0);
qproperty-iconSize:15;
qproperty-bgHeight:8;
        }
            ''')

        self.vboy = QVBoxLayout(self)
        self.vboy.addWidget(self.sl)

    def test(self,v):
        print("v:",v)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())