from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QPushButton
)

from PyQtGuiLib.styles import StyleLinker

class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800,600)

        self.btn = QPushButton("测试1",self)
        self.btn.setStyleSheet('''
        QPushButton{
        background-color: rgb(255, 85, 127);
        }
        QPushButton:hover{
        background-color: rgb(0, 85, 127);
        }
        ''')
        self.btn.setGeometry(100,100,300,300)


        self.styleLinker = StyleLinker()
        self.styleLinker.addQObject(self.btn)
        self.styleLinker.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())