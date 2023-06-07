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

from typing import TypeVar

Head_Type = TypeVar("Head_Type",str,bytes)


class HeadImage(QLabel):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def setHeadImage(self,data:Head_Type):
        if isinstance(data,bytes):
            image = QImage()
            image.loadFromData(data)
            pix = QPixmap()
            fimage = pix.fromImage(image)
            image_pix = fimage.scaled(self.size())
            self.setPixmap(image_pix)
        elif isinstance(data,str):
            image = QImage()
            image.load(data)
            pix = QPixmap()
            fimage = pix.fromImage(image)
            image_pix = fimage.scaled(self.size())
            self.setPixmap(image_pix)
