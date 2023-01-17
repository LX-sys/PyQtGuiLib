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

        self.cp = ColorPalette(self)
        self.cp.setStyleMode(ColorPalette.Style_White)
        self.cp.move(10,10)
        self.cp.clicked.connect(lambda t,c:print(t,c))
        self.cp.colorNamed.connect(self.test)

    def test(self,rgba):
        print("-->",self.cp.getRGBA())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test_ColorPalette()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())