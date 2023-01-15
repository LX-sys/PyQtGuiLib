from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget
)

'''
    开关按钮 测试用例
'''
from random import randint
from PyQtGuiLib.core.switchButtons import SwitchButton
from PyQtGuiLib.core import FlowLayout

class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

        self.flow = FlowLayout(self)

        # ---
        swbtn = SwitchButton()
        swbtn.setDefaultState(False)
        swbtn.setFixedSize(60, 30)
        # swbtn.show()
        self.flow.addWidget(swbtn)

        swbtn1 = SwitchButton()
        swbtn1.setShape(SwitchButton.Shape_Square)
        swbtn1.setDefaultState(False)
        swbtn1.setFixedSize(60, 30)
        # swbtn.show()
        self.flow.addWidget(swbtn1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())