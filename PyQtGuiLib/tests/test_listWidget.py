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


from PyQtGuiLib.tests.temp_tests.index_history_item import Ui_HistoryItem

class TestListWidget(ListWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,500)

        # self.listw = ListWidget(self)
        # self.listw.resize(600,500)
        # self.listw.move(100,100)
        # self.listw.itemDoubleClicked.connect(lambda :print("asd"))

        for i in range(5):
            widget = Ui_HistoryItem()
            widget.setStyleSheet(ButtonStyle.randomStyle())
            self.addWidget(widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TestListWidget()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())