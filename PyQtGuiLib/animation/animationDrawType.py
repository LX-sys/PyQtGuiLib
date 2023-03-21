# -*- coding:utf-8 -*-
# @time:2023/3/1715:33
# @author:LX
# @file:animationDrawType.py
# @software:PyCharm

'''
    这个类为绘图动画的封装类型
'''
import typing
from PyQtGuiLib.header import (
    QColor,
    QRect
)

Any = typing.Any
'''

后续这里的值需要改成float类型
'''

# 值类型
class AniNumber:
    def __init__(self,n):
        self.__n = n

    def setNumber(self,n):
        self.__n = n

    def value(self)->int:
        return self.__n

    # 这里表示任意类型
    def type(self) -> Any:
        return type(self.value())


# 多值类型
class AniNumbers:
    def __init__(self,*args):
        self.__an = []
        if args:
            self.setNumbers(*args)

    def setNumbers(self,*args):
        for an in args:
            self.__an.append(AniNumber(an))

    def type(self) -> list:
        return list

    def numberObjs(self) -> list:
        return [n for n in self.__an]

    def values(self) -> list:
        return [n.value() for n in self.__an]


# 颜色类型
class AniColor(AniNumbers):
    def __init__(self,r:int,g:int,b:int,a:int=255):
        if r < 0 or r >255 or g <0 or g>255 or b <0 or b>255 or b <0 or b >255\
            or a <0 or a > 255:
            raise Exception("The value ranges from 0 to 255!")
        super().__init__(r,g,b,a)

    def type(self) -> QColor:
        return QColor

    def values(self) -> QColor:
        return QColor(*super().values())


# 矩形类型
class AniRect(AniNumbers):
    def __init__(self,x:int,y:int,w:int,h:int):
        super().__init__(x,y,w,h)

    def type(self) -> QRect:
        return QRect

    def values(self) -> QRect:
        return QRect(*super().values())