from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QPushButton
)

'''
   调色板 测试用例
'''

from PyQtGuiLib.core import ColorPalette

class Test_ColorPalette(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

        self.btn = QPushButton("弹出调色版",self)
        self.btn.clicked.connect(self.test)


        self.cp = ColorPalette()
        self.cp.move(10,10)

    def test(self):
        self.cp.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test_ColorPalette()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())