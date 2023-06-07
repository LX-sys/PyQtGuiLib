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
    QScrollArea,
    QVBoxLayout,
    Qt
)

from PyQtGuiLib.core.charRooms.transmitter import Transmitter
from PyQtGuiLib.core.charRooms.message import (
    MessageBody,BGTemplate,Message,
    Left,Right,Type_Text,Type_Image
)

'''
    聊天对话框组件
'''


class ChatRoom(QScrollArea):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(500,500)
        self.setWindowTitle("ChatRoom")

        self.body = QWidget()
        self.vlay = QVBoxLayout(self.body)
        self.vlay.setAlignment(Qt.AlignTop)
        self.vlay.setContentsMargins(0,0,0,0)
        self.vlay.setSpacing(0)

        self.body.setStyleSheet("background-color:#fff;")

        self.setWidget(self.body)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.defaultStyle()

    def addWidget(self,widget:QWidget):
        self.vlay.addWidget(widget)

    def createBGWidget(self,direction,mes:Message):
        widget = BGTemplate(self,direction,mes)
        self.addWidget(widget)
        self.scrollBottom(widget.height())

    # 滚动条置底
    def scrollBottom(self,h=140):
        dif = self.verticalScrollBar().height()-self.body.height()
        dif = abs(dif)
        if dif:
            self.verticalScrollBar().setMaximum(dif+h)
            self.verticalScrollBar().setValue(dif+h)

    def sendText(self,mes:Message) -> bool:
        if len(mes.data()) > mes.getMaxMesNum():
            return False
        self.createBGWidget(Right, mes)
        return True

    def receiveText(self,mes:Message) -> bool:
        if len(mes.data()) > mes.getMaxMesNum():
            return False
        self.createBGWidget(Left, mes)
        return True

    def resizeEvent(self, e) -> None:
        self.scrollBottom()
        super().resizeEvent(e)

    def defaultStyle(self):
        self.setStyleSheet('''
QScrollBar:horizontal{
padding:0px;
max-height:12px;
padding:2px;
}
QScrollBar:vertical{
padding:0px;
max-width:10px;
padding:2px;
}
QScrollBar::handle{
background-color: rgb(39, 39, 39);
border-radius:2px;
}
QScrollBar::handle:hover{
background-color: rgb(72, 72, 72);
border:1px solid rgb(149, 149, 149);
}
QScrollBar::add-page,QScrollBar::sub-page {
background:rgb(57, 57, 57);
}
QScrollBar::sub-line,QScrollBar::add-line {
background:none;
}
        ''')


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

    def send_event(self,text):
        if text:
            mes = Message(None,text)
            mes.setHeadImage(r"C:\Users\Administrator\Downloads\机器小狗-removebg-preview.png")
            self.chat.sendText(mes)

    def receive_event(self,text):
        if text:
            mes = Message("铁蛋",text)
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