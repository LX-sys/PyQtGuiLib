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

from PyQtGuiLib.core import Slider

'''
    测试用例的标准模板,该代码用于复制
'''


class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

        self.sl = Slider(self)
        self.sl.resize(300,30)
        self.sl.move(100,100)

        self.sl.setValue(0)
        # self.sl.setPercentageValue(100)

        self.sl.setBuffPercentageValue(80)
        self.sl.valueChanged.connect(self.test)

        self.sl.setStyleSheet('''
        Slider{
qproperty-radius:5;
qproperty-margin:3;
qproperty-backgroundColor:rgb(200, 200, 200);
qproperty-iconBackgroundColor:rgb(200, 100, 200);
qproperty-sliderH:15;
qproperty-iconSize:20;
        }
            ''')

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