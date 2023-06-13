# -*- coding:utf-8 -*-
# @time:2023/6/818:14
# @author:LX
# @file:utility.py
# @software:PyCharm
from PyQtGuiLib.header import (
    QImage,
    QPixmap,
    QSize
)

from typing import TypeVar

Head_Type = TypeVar("Head_Type",str,bytes)


def imageToPix(data:Head_Type,size):
    image = QImage()
    if isinstance(data, bytes):
        image.loadFromData(data)
    elif isinstance(data, str):
        image.load(data)
    pix = QPixmap()
    fimage = pix.fromImage(image)
    return fimage.scaled(size)
