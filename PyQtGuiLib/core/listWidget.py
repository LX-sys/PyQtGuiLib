from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QListWidget,
    QListWidgetItem,
    QWidget,
    QSize,
    QStyledItemDelegate
)


'''

    QListWidget 增强版本
'''

class ListWidgetItem(QListWidgetItem):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

class ListWidget(QListWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def addWidget(self,widget:QWidget):
        item = ListWidgetItem()
        self.addItem(item)
        self.setItemWidget(item, widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ListWidget()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())