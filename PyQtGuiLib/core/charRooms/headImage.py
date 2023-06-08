# -*- coding:utf-8 -*-
# @time:2023/6/518:19
# @author:LX
# @file:headImage.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    Qt,
    QImage,
    QPixmap
)
from PyQtGuiLib.core.charRooms.utility import imageToPix,Head_Type


class HeadImage(QLabel):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def setHeadImage(self,data:Head_Type):
        self.setPixmap(imageToPix(data,self.size()))
