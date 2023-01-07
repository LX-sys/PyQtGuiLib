from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QPushButton,
    QWidget
)

from PyQtGuiLib.styles import ButtonStyle

class TestStyle(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800, 500)

        x = 50
        for i in range(5):
            btn = QPushButton("test_{}".format(str(i)), self)
            btn.setGeometry(x, 100, 130, 60)
            x+=150
            btn.setStyleSheet(ButtonStyle.contrastStyle())

        # self.btn = QPushButton("test",self)
        # self.btn.setGeometry(100,100,130,60)
        #
        # self.btn2 = QPushButton("test2",self)
        # self.btn2.setGeometry(250,100,130,60)
        #
        # self.btn.setStyleSheet(ButtonStyle.flatStyle(None,radius="10%"))
        # # self.btn2.setStyleSheet(ButtonStyle.outlineStyle(None,radius="10%"))
        # self.btn2.setStyleSheet(ButtonStyle.randomStyle())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TestStyle()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())