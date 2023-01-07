from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QPushButton,
    QSize,
    QRect
)
from PyQt5.QtWidgets import QLayout,QLayoutItem
'''
    简单的流式布局
'''

class FlowLayout(QLayout):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.items = []


    def addItem(self, item: QLayoutItem) -> None:
        print("==>",item)
        self.items.append(item)

    def count(self) -> int:
        return len(self.items)

    def itemAt(self, index: int) -> QLayoutItem:
        if index < self.count():
            return self.items[index]

    def takeAt(self, index: int) -> QLayoutItem:
        return index >= 0 and index < self.count() if self.takeAt(index) else 0

    def spacing(self) -> int:
        return 0

    def setGeometry(self, r:QRect):
        super().setGeometry(r)
        if self.count() == 0:
            return
        w = r.width() - (self.count() - 1) * self.spacing()
        h = r.height() - (self.count() - 1) * self.spacing()
        i = 0

        while i < self.count():
            o = self.items[i]
            geom = QRect(r.x() + i * self.spacing(), r.y() + i * self.spacing(), w, h)
            o.setGeometry(geom)
            i = i + 1

    def sizeHint(self):
        s = QSize(0, 0)
        n = self.count()
        if n > 0:
            s = QSize(100, 70)  # start with a nice default size
        i = 0
        while i < n:
            o = self.items[i]
            s = s.expandedTo(o.sizeHint())
            i = i + 1
        return s + n * QSize(self.spacing(), self.spacing())

    def minimumSize(self):
        s = QSize(0, 0)
        n = self.count()
        i = 0
        while i < n:
            o = self.items[i]
            s = s.expandedTo(o.minimumSize())
            i = i + 1
        return s + n * QSize(self.spacing(), self.spacing())

class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

        self.flow = FlowLayout(self)
        btn = QPushButton("asd")
        btn.resize(130,60)
        btn2 = QPushButton("112")
        btn2.resize(130, 60)
        self.flow.addWidget(btn)
        self.flow.addWidget(btn2)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())