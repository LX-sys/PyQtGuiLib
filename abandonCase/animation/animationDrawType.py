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
    QRect,
    QPoint
)

Any = typing.Any
Color = typing.TypeVar("Color",int,QColor)
Rect = typing.TypeVar("Rect",int,QRect)
Point = typing.TypeVar("Point",int,QPoint)

# 值类型
class AniNumber:
    def __init__(self,n:Any):
        self.__n = n

    def setNumber(self,n:Any):
        self.__n = n

    def value(self)->Any:
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
    def __init__(self,r:Color,g:int,b:int,a:int=255):
        if isinstance(r,QColor):
            value = QColor(*r.getRgb())
        elif 0 <= r and r <= 255 and\
             0 <= g and g <= 255 and\
             0 <= b and b <= 255 and\
             0 <= a and a <= 255:
                value = r,g,b,a
        else:
            raise Exception("The value ranges from 0 to 255!")
        super().__init__(*value)

    def type(self) -> QColor:
        return QColor

    def values(self) -> QColor:
        return QColor(*super().values())


# 矩形类型
class AniRect(AniNumbers):
    def __init__(self,x:Rect,y:int,w:int,h:int):
        if isinstance(x,QRect):
            value = x.getRect()
        else:
            value = x,y,w,h
        super().__init__(*value)

    def type(self) -> QRect:
        return QRect

    def values(self) -> QRect:
        return QRect(*super().values())

# 点类型
class AniPoint(AniNumbers):
    def __init__(self, x:Point, y: int):
        if isinstance(x, QPoint):
            value = x.x(),x.y()
        else:
            value = x, y
        super().__init__(*value)

    def type(self) -> QPoint:
        return QPoint

    def values(self) -> QPoint:
        return QPoint(*super().values())


# 阴影类型(测试中)
class AniShadow(AniNumbers):
    def __init__(self,offx:int,offy:int,r:int,color:QColor):
        super().__init__(offx,offy,r,color)

    def type(self) -> str:
        return "shadow"

    def values(self) -> list:
        return [*super().values()]