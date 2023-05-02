from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QLabel
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 设置为可拖拽
        self.setAcceptDrops(True)

        # 垂直布局
        layout = QVBoxLayout(self)

        # 列表框
        self.list_widget = QListWidget(self)
        self.list_widget.addItems(['item 1', 'item 2', 'item 3'])
        self.list_widget.setDragEnabled(True)
        layout.addWidget(self.list_widget)

    def dragEnterEvent(self, event):
        # 接受拖拽操作，只接受文本
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        # 接受拖拽操作
        if event.mimeData().hasText():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        # 接受拖拽操作，创建QLabel
        if event.mimeData().hasText():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            # 获取文本
            text = event.mimeData().text()

            # 创建QLabel
            label = QLabel(text, self)
            label.move(event.pos())
            label.show()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication([])
    widget = MyWidget()
    widget.show()
    app.exec_()
