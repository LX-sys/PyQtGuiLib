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
    QComboBox
)

'''
    测试用例的标准模板,该代码用于复制
'''
from PyQtGuiLib.core.resolver import dumpStructure

class Test(QMainWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

        self.setStyleSheet('''
QMainWindow[color="green"]{
background-color: rgb(126, 255, 118);
}
QMainWindow[color="red"]{
background-color: rgb(255, 0, 52);
}
        ''')
        self.btn = QPushButton("green",self)
        self.btn2 = QPushButton("red",self)
        self.btn.move(30,30)
        self.btn2.move(80,30)

        self.btn.clicked.connect(self.test1)
        self.btn2.clicked.connect(self.test2)
        # self.setProperty("color", "green")

    def test1(self):
        self.setProperty("color", "green")
        self.setStyleSheet(self.styleSheet())

    def test2(self):
        self.setProperty("color", "red")
        self.setStyleSheet(self.styleSheet())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())