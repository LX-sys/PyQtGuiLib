# -*- coding:utf-8 -*-
# @time:2023/6/518:07
# @author:LX
# @file:message.py
# @software:PyCharm
from PyQtGuiLib.header import (
    QWidget,
    QFrame,
    QPushButton,
    textSize,
    QFont,
    Qt,
    QLineEdit,
    QLabel,
    QIcon,
    QSize,
    QPixmap
)
import re
import time

from PyQtGuiLib.core.charRooms.headImage import HeadImage

Left = "left"
Right = "right"

Type_Text = "text"
Type_Image = "image"


class Message:
    def __init__(self, name, data, type="text"):
        '''
        {
            "data":xxxx
            "name":xxx
            "type":xxxx
        }

        :param data:
        '''
        self.__data = {
            "name": name,
            "data": data,
            "type": type,
            "send_time":"",
            "head_image": {
                "path": "",
            }
        }

        self.Max_Line_Num = 50  # 单行最大文本数量

        self.Max_Message_Num = 2000  # 单条消息的最大字数

        self.bgTemplate = None

    def setHeadImage(self, path: str):
        self.__data["head_image"]["path"] = path

    def headImage(self) -> dict:
        return self.__data["head_image"]

    def isHeadImage(self) -> bool:
        return True if self.headImage()["path"] else False

    def getMaxMesNum(self) -> int:
        return self.Max_Message_Num

    def name(self) -> str:
        self.__data["send_time"] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        return self.__data["name"] + " {}".format(time.strftime("%H:%M:%S", time.localtime()))

    def dataType(self) -> str:
        return self.__data["type"]

    def data(self):
        return self.__data["data"]

    def length(self) -> int:
        return len(self.data())

    def setBGTemplate(self, obj):
        self.bgTemplate = obj

    def getMaxStr(self, text_list) -> str:
        max_len = 0
        data = ""
        for text in text_list:
            n = len(text)
            if n > max_len:
                max_len = n
                data = text
        return data

    # 单行文本对折
    def strFoldHalf(self, str_text) -> str:
        if len(str_text) < self.Max_Line_Num:
            return None
        else:
            temp_texts = []
            s, e = 0, self.Max_Line_Num
            while True:
                data = str_text[s:e]
                if data:
                    temp_texts.append(data)
                else:
                    return temp_texts
                s = e
                e += self.Max_Line_Num

    def analysisText(self):
        text = self.data()
        newline_character_number = 1

        period_text = text.split("\n")

        # ---
        '''
            对文本折行,
            如果文本只有一句话,则单行最大文字数量为 60
            如果是多行,
                在多行中,根据文章和的语言进行区分 单行最大文字数量
                中文 > 英文 单行最大文字数量为 30
              反之:
                单行最大文字数量为 60

        '''
        chinese_data = re.findall(r"[\u4e00-\u9fa5]+", text)
        en_data = re.findall(r"[a-z]+", text, re.I)
        if chinese_data:
            chinese_num = len("".join(chinese_data))
        else:
            chinese_num = 0
        if en_data:
            en_num = len("".join(en_data))
        else:
            en_num = 0

        if len(period_text) == 1:
            if chinese_num > en_num:
                self.Max_Line_Num = 30
            else:
                self.Max_Line_Num = 60
            re_text = self.strFoldHalf(text)
            if re_text:
                period_text.clear()
                period_text.extend(re_text)
                self.__data["data"] = "\n".join(period_text)
        else:
            if chinese_num > en_num:
                self.Max_Line_Num = 30
            else:
                self.Max_Line_Num = 50

            new_period_text = []
            for nt in period_text:
                re_text = self.strFoldHalf(nt)
                if not re_text:
                    new_period_text.append(nt)
                else:
                    new_period_text.extend(re_text)
            self.__data["data"] = "\n".join(new_period_text)
            period_text = new_period_text
        # ===
        if "\n" in self.data():
            newline_character_number = len(period_text) + 1

        max_period_text = self.getMaxStr(period_text)

        f = QFont(max_period_text)
        f.setPointSize(12)
        fsize = textSize(f, max_period_text)

        w, h = fsize.width() + 13, fsize.height() * newline_character_number + 5
        if h < 30:
            h = 30
        # print("宽度,高度:", w, h)

        self.__data["BGTemplate_Height"] = h + self.bgTemplate.profile_btn.height() + self.bgTemplate.profile_btn.pos().y()
        self.__data["MessageBody_Size"] = w, h

    def bgTemplateHeight(self) -> int:
        return self.__data["BGTemplate_Height"]

    def messageBodySize(self) -> tuple:
        return self.__data["MessageBody_Size"]


# 消息内容主体
class MessageBody(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mes = None  # type:# Message
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.setOpenExternalLinks(True)
        self.setTextInteractionFlags(Qt.LinksAccessibleByMouse | Qt.TextSelectableByMouse)

        f = QFont()
        f.setPointSize(12)
        self.setFont(f)

        self.setStyleSheet('''
        border:1px solid rgb(184, 184, 184);
        border-radius:5px;
        font: 12pt "等线";
        background-color: rgb(255, 170, 127);
        padding-left:5;
        padding-top:5;
                ''')

    def setMes(self, mes: Message):
        text = mes.data()
        if re.findall("^http.*|^http.* ", text):
            self.setText("<a href='{}'>{}</a>".format(text, text))
        else:
            self.setText("{}".format(text))


# 单条消息模板
class BGTemplate(QFrame):
    def __init__(self, parent, direction, mes: Message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent

        self.setStyleSheet("background-color:#fff;")

        self.profile_btn = HeadImage(self)
        self.profile_btn.setFixedSize(50, 50)
        if mes.isHeadImage():
            self.profile_btn.setHeadImage(mes.headImage()["path"])

        mes.setBGTemplate(self)
        mes.analysisText()
        self.setFixedHeight(mes.bgTemplateHeight())

        #
        self.mes = MessageBody(self)
        self.mes.setMes(mes)
        self.direction = direction

        if direction == Left:
            self.moveLeft()
            self.name = QLabel(self)
            self.name.setText(mes.name())
            self.name.setStyleSheet('font: 25 10pt "等线 Light";')
            self.name.move(self.profile_btn.width() + 15, self.profile_btn.height() // 2 - 10)
        elif direction == Right:
            self.mes.show()
            self.moveRight()

        self.defaultStyle()

    def moveLeft(self):
        self.profile_btn.move(0, 10)
        self.mes.move(self.profile_btn.width() + 15, self.profile_btn.height() // 2 + 10)

    def moveRight(self):
        self.profile_btn.move(self.parent.width() - self.profile_btn.width() - 20, 10)
        self.mes.move(self.width() - self.mes.width() - self.profile_btn.width() - 25,
                      self.profile_btn.height() // 2 + 10)

    def defaultStyle(self):
        self.profile_btn.setStyleSheet('''
border:1px solid rgb(184, 184, 184);
border-radius:25px;
        ''')

    def resizeEvent(self, e) -> None:
        if self.direction == Right:
            self.moveRight()
        super().resizeEvent(e)