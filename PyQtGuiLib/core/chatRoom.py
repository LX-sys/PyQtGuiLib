# -*- coding:utf-8 -*-
# @time:2023/5/3117:55
# @author:LX
# @file:chatRoom.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QListWidget,
    QListWidgetItem,
    QPushButton
)


'''
    聊天对话框组件
'''


class ChatRoom(QListWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(500,500)
        self.setWindowTitle("ChatRoom")

        item = QListWidgetItem()

        self.btn = QPushButton()
        self.btn.setFixedWidth(100)
        self.btn.setStyleSheet("background-color:red;")
        self.btn.setText("测试")

        self.addItem(item)
        self.setItemWidget(item,self.btn)




if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = ChatRoom()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())