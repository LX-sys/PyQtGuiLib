# -*- coding:utf-8 -*-
# @time:2023/6/818:19
# @author:LX
# @file:test.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QVBoxLayout,
    Qt
)

from PyQtGuiLib.core.charRooms.chatRoom import ChatRoom,Transmitter,Message



class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setWindowTitle("聊天组件")
        self.resize(800,500)
        self.vlay = QVBoxLayout(self)

        self.chat = ChatRoom()

        self.rb = Transmitter()
        self.lb = Transmitter()

        # https://www.baidu.com/
        self.vlay.addWidget(self.chat)
        self.vlay.addWidget(self.lb)
        self.vlay.addWidget(self.rb)

        self.rb.texted.connect(self.send_event)
        self.lb.texted.connect(self.receive_event)

    def send_event(self,data):
        if data:
            mes = Message(None, data)
            mes.setHeadImage(r"C:\Users\Administrator\Downloads\机器小狗-removebg-preview.png")
            self.chat.sendText(mes)

    def receive_event(self,data):
        if data:
            mes = Message("铁蛋",data)
            mes.setHeadImage(r"C:\Users\Administrator\Downloads\1-removebg-preview.png")
            self.chat.receiveText(mes)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())