from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QPushButton,
    QLabel,
    QObject,
    qt,
    QGroupBox,
    QTreeWidgetItem,
    QLineEdit
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
        self.l2 = QLabel("我是标签",self)
        self.btn.move(10,10)
        self.l2.move(40,40)
        self.line = QLineEdit(self)
        self.line.move(10,80)

        self.styleLinker = StyleLinker()
        self.styleLinker.addQObjects([self.btn,self.l2,self.line])
        self.styleLinker.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())