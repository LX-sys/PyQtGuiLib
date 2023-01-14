from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget
)

from PyQtGuiLib.core.lineedit import DynamicTLine

'''
    动态 标题输入框 测试用例
'''

class Test_DynamicTLine(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

        self.line = DynamicTLine(self)
        self.line.setPlaceholderText("hello")
        self.line.move(100,100)

        self.line2 = DynamicTLine(self)
        self.line2.move(100,300)
        self.line.setPlaceholderText("asdsa")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test_DynamicTLine()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())