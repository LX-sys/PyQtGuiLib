from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag


class SourceListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSelectionMode(self.SingleSelection)



    def startDrag(self, supportedActions):
        item = self.currentItem()
        if item is not None:
            drag = QDrag(self)
            mimeData = QMimeData()
            mimeData.setText(item.text())
            drag.setMimeData(mimeData)
            drag.exec_(Qt.CopyAction)


class TargetWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setStyleSheet('''border:1px solid blue;''')

        self.setMinimumHeight(50)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            pos = event.pos()
            text = event.mimeData().text()
            button = QPushButton(text, self)
            button.move(pos)
            button.show()
            event.accept()
        else:
            event.ignore()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Drag and Drop')
        self.setGeometry(200, 200, 400, 300)

        self.sourceListWidget = SourceListWidget(self)
        self.targetWidget = TargetWidget()

        layout = QVBoxLayout(self)
        layout.addWidget(self.sourceListWidget)
        layout.addWidget(self.targetWidget)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
