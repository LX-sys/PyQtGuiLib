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
    QFrame,
    QPushButton,
    QPainter,
    textSize,
    QFont,
    QScrollArea,
    QVBoxLayout,
    Qt,
    QLineEdit,
    QLabel,
    QTextBrowser,
    QFontMetricsF
)
import time

from PyQtGuiLib.core.charRooms.transmitter import Transmitter

Left = "left"
Right = "right"

Type_Text = "text"
Type_Image = "image"


class Message:
    def __init__(self,name,data,type="text"):
        '''
        {
            "data":xxxx
            "name":xxx
            "type":xxxx
        }

        :param data:
        '''
        self.__data = {
            "name":name,
            "data":data,
            "type":type,
            "head_picture":""
        }

        self.bgTemplate = None

    def name(self) -> str:
        return self.__data["name"]+" {}".format(time.strftime("%H:%M:%S",time.localtime()))

    def dataType(self) -> str:
        return self.__data["type"]

    def data(self):
        return self.__data["data"]

    def length(self) -> int:
        return len(self.data())

    def setBGTemplate(self,obj):
        self.bgTemplate = obj

    def analysisText(self):
        text = self.data()
        period_text = text.split("\n")

        newline_character_number = 1

        if "\n" in text:
            newline_character_number = len(period_text)

        max_period_text = max(period_text)

        f = QFont(max_period_text)
        f.setPointSize(11)
        fsize = textSize(f,max_period_text)
        metr = QFontMetricsF(f)
        fsize = metr.size(Qt.TextWordWrap,max_period_text)
        print(fsize)
        # metrics = QFontMetricsF(font)
        # bounding_rect = metrics.boundingRect(0, 0, self.width(), self.height(), Qt.TextWordWrap, max_period_text)
        w,h = fsize.width(), fsize.height()*newline_character_number+10
        if h < 30:
            h = 30
        print(w,h)

        self.__data["BGTemplate_Height"] = h+self.bgTemplate.profile_btn.height()+self.bgTemplate.profile_btn.pos().y()
        self.__data["MessageBody_Size"] = w,h

    def bgTemplateHeight(self) -> int:
        return self.__data["BGTemplate_Height"]
    
    def messageBodySize(self)->tuple:
        return self.__data["MessageBody_Size"]


# 消息内容主体
class MessageBody(QLabel):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.mes = None  # type:Message
        self.resize(200, 70)
        self.setAlignment(Qt.AlignCenter)

        self.setOpenExternalLinks(True)
        self.setWordWrap(True)

        self.setStyleSheet('''
    border:1px solid rgb(184, 184, 184);
    border-radius:5px;
    font: 11pt "等线";
    padding-left:0;
            ''')

    def setMes(self, mes: Message):
        self.mes = mes
        self.resize(*mes.messageBodySize())
        text = mes.data()
        if "http" in text or "https" in text:
            self.setText("<a href=\"{}\">{}</a>".format(text,text))
        else:
            self.setText("{}".format(mes.data()))


# 单条消息模板
class BGTemplate(QFrame):
    def __init__(self,parent,direction,mes:Message,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.parent = parent

        self.setStyleSheet("background-color:#fff;")

        self.profile_btn = QPushButton(self)
        self.profile_btn.setFixedSize(50,50)
        self.profile_btn.setText("头像")

        mes.setBGTemplate(self)
        mes.analysisText()
        self.setFixedHeight(mes.bgTemplateHeight())

        #
        self.mes = MessageBody(self)
        self.mes.setMes(mes)
        self.mes.setStyleSheet('''
border:1px solid rgb(184, 184, 184);
border-radius:5px;
font: 11pt "等线";
background-color: rgb(255, 170, 127);
        ''')

        self.direction = direction

        if direction == Left:
            self.moveLeft()
            self.name = QLabel(self)
            self.name.setText(mes.name())
            self.name.setStyleSheet('font: 25 10pt "等线 Light";')
            self.name.move(self.profile_btn.width()+15,self.profile_btn.height()//2-10)

        elif direction == Right:
            self.moveRight()

        self.defaultStyle()

    def moveLeft(self):
        self.profile_btn.move(0,10)
        self.mes.move(self.profile_btn.width()+15,self.profile_btn.height()//2+10)

    def moveRight(self):
        self.profile_btn.move(self.parent.width()-self.profile_btn.width()-20, 10)
        self.mes.move(self.width()-self.mes.width()-self.profile_btn.width()-25, self.profile_btn.height()//2+10)

    def defaultStyle(self):
        self.profile_btn.setStyleSheet('''
border:1px solid rgb(184, 184, 184);
background-color: rgb(85, 255, 255);
border-radius:25px;
font: 11pt "等线";
        ''')

    def resizeEvent(self, e) -> None:
        if self.direction == Right:
            self.moveRight()
        super().resizeEvent(e)


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
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.defaultStyle()

    def addWidget(self,widget:QWidget):
        self.vlay.addWidget(widget)

    def createBGWidget(self,direction,mes:Message):
        widget = BGTemplate(self,direction,mes)
        self.addWidget(widget)
        self.scrollBottom()

    # 滚动条置底
    def scrollBottom(self):
        dif = self.verticalScrollBar().height()-self.body.height()
        dif = abs(dif)
        if dif:
            self.verticalScrollBar().setMaximum(dif+140)
            self.verticalScrollBar().setValue(dif+140)

    def sendText(self,mes:Message):
        self.createBGWidget(Right,mes)

    def receiveText(self,mes:Message):
        self.createBGWidget(Left, mes)

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
max-width:12px;
padding:2px;
}
QScrollBar::handle{
background-color: rgb(39, 39, 39);
border-radius:4%;
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
            self.chat.sendText(mes)

    def receive_event(self,text):
        if text:
            mes = Message("铁蛋",text)
            self.chat.receiveText(mes)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())