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
    QVBoxLayout
)

from PyQtGuiLib.core import Slider
'''
    测试 滑块
'''


class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

        self.sl = Slider(self)
        self.sl.move(50,50)
        self.sl.resize(300,40)
        # self.sl.setValue(50)
        # self.sl.setBuffValue(80)
        self.sl.setStyleSheet('''
        Slider{
qproperty-radius:4;
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