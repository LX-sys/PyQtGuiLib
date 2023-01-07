from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QWidget,
    QThread,
    Signal,
    QColor,
    QSlider,
    QListWidgetItem
)

from PyQtGuiLib.core import ListWidget
from PyQtGuiLib.styles import ButtonStyle


class TestListWidget(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800,600)

        self.listw = ListWidget(self)
        self.listw.resize(200,300)
        self.listw.move(100,100)

        for i in range(5):
            widget = QWidget()
            widget.setFixedHeight(50)
            widget.setStyleSheet(ButtonStyle.randomStyle())
            self.listw.addWidget(widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TestListWidget()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())