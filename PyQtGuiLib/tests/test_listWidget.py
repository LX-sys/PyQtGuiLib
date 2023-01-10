from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QWidget,
    QThread,
    Signal,
    QColor,
    QSlider,
    QListWidgetItem,
    QLabel,
    qt
)

from PyQtGuiLib.core import ListWidget
from PyQtGuiLib.styles import ButtonStyle


class TestListWidget(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800,700)

        self.listw = ListWidget(self)
        self.listw.resize(600,500)
        self.listw.move(100,100)
        self.listw.itemDoubleClicked.connect(lambda :print("asd"))

        for i in range(30):
            widget = QLabel(str(i))
            widget.setAlignment(qt.AlignCenter)
            widget.setStyleSheet(ButtonStyle.randomStyle())
            self.listw.addWidget(widget)

        wid = self.listw.getAllWidget()[1]
        print(wid)
        # self.listw.removeItemWidget(self.listw.widgets[0][0])
        # self.listw.adjustSize()
        self.listw.removeWidget(wid)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TestListWidget()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())