# -*- coding:utf-8 -*-
# @time:2023/3/2011:39
# @author:LX
# @file:animationLayout.py
# @software:PyCharm

from PyQtGuiLib.header import (
    QPaintEvent,
    QRect
)

'''
    
    动画上的布局
'''


class AnimationLayout:
    def __init__(self,pe:QPaintEvent):
        self.__pe = pe

        #
        self.__minHeight = 23

        self.__space = 6

        self.__topMargin = 9
        self.__bottomMargin = 9
        self.__leftMargin = 9
        self.__rightMargin = 9

        self.__draw_list = []
        print(self.rect())

    def rect(self) -> QRect:
        return self.__pe.rect()

    def minHeight(self) -> int:
        return self.__minHeight

    def setMinHeight(self,h:int):
        self.__minHeight = h

    def space(self) -> int:
        return self.__space

    def setSpace(self,v:int):
        self.__space = v

    def setContentsMargins(self,top,bottom,left,right):
        self.__topMargin = top
        self.__bottomMargin = bottom
        self.__leftMargin = left
        self.__rightMargin = right

    def contentsMargins(self)->tuple:
        return self.__topMargin,self.__bottomMargin,self.__leftMargin,self.__rightMargin

    # 子类重写函数
    def __addDraw__(self,graph,*args):
        return

    # 调用函数
    def addDraw(self,graph,*args):
        self.__draw_list(self.__addDraw__(graph,*args))

    def count(self) -> int:
        return self.__draw_list

    def isEmpty(self) -> bool:
        return False if self.__draw_list else True

    def drawAt(self,i:int):
        return self.__draw_list[i]