from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QPushButton,
)
from random import randint
from PyQtGuiLib.core import FlowLayout
from PyQtGuiLib.styles import ButtonStyle
'''
    流式布局 测试用例
'''

class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)
        self.setWindowTitle("流式布局 测试用例")

        self.items = []

        # 流式布局
        self.flow = FlowLayout(self)

        # 创建 50 个 按钮
        for i in range(50):
            btn = QPushButton("test_{}".format(i))
            btn.setFixedSize(130,randint(40,60))
            btn.setStyleSheet(ButtonStyle.randomStyle())  # 使用 皮肤包
            self.items.append(btn)
            self.flow.addWidget(btn)

        # 删除前 5 个按钮
        for i in range(5):
            self.flow.removeWidget(self.items[i])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())