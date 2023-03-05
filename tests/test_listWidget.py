from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QWidget,
    QLabel,
    qt,
    QPushButton,
    uuid
)
'''
    QListWidget 增强版本-ListWidget 测试用例
'''

from PyQtGuiLib.core import ListWidget
from PyQtGuiLib.styles import ButtonStyle


class TestListWidget(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800,700)

        self.btn = QPushButton("动态添加",self)
        self.btn.move(10,10)
        self.btn.clicked.connect(self.addLabel)

        self.delt = QPushButton("动态删除", self)
        self.delt.move(180, 10)
        self.delt.clicked.connect(self.delLabel)

        # 增强版本-ListWidget
        self.listw = ListWidget(self)
        # self.listw.setAniEnabled(False) #  取消动画
        self.listw.resize(600,500)
        self.listw.move(100,100)
        self.listw.itemDoubleClicked.connect(lambda :print("asd"))

        for i in range(5):
            widget = QLabel(str(i))
            widget.setAlignment(qt.AlignCenter)
            widget.setStyleSheet(ButtonStyle.contrastStyle())
            self.listw.addWidget(widget)

    def addLabel(self):
        l = QLabel(str(uuid.uuid1()))
        l.setAlignment(qt.AlignCenter)
        l.setStyleSheet(ButtonStyle.contrastStyle())
        self.listw.addWidget(l)


    def delLabel(self):
        wid = self.listw.getAllWidget()[2]
        self.listw.removeWidget(wid)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TestListWidget()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())