from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QLabel
)

from PyQtGuiLib.styles import StyleLinker

class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800,600)

        self.setStyleSheet('''
background-color: rgb(0, 0, 0);
        ''')

        self.l = QLabel("我是标签",self)
        self.l.setGeometry(100,100,300,300)


        self.styleLinker = StyleLinker()
        self.styleLinker.addQObject(self.l)
        self.styleLinker.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())