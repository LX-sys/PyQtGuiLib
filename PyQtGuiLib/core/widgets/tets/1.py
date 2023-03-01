from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem

app = QApplication([])

list_widget = QListWidget()

# list_widget.setro
list_widget.setFlow(QListWidget.LeftToRight)
list_widget.setResizeMode(QListWidget.Adjust)

for i in range(10):
    item = QListWidgetItem(f"Item {i}")
    list_widget.addItem(item)

list_widget.show()
app.exec_()
