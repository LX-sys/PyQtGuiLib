# -*- coding:utf-8 -*-
# @time:2023/4/198:53
# @author:LX
# @file:animation.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QWidget
)
from typing import Callable,Any,TypeVar,List,Union,Tuple
from PyQtGuiLib.animation.new_animation.PropertyAnimation import ParallelAnimationGroup,SequentialAnimationGroup,PropertyAnimation


AnimationGroup = TypeVar("AnimationGroup",ParallelAnimationGroup,SequentialAnimationGroup)
'''
    动画框架重写
'''


class Animation:
    Parallel = 1
    Sequential = 2

    def __init__(self,):
        # self.__paralle = ParallelAnimationGroup()
        # self.__sequen = SequentialAnimationGroup()

        self.__startMode = SequentialAnimationGroup()  # 默认串行
        self.__anis = []  # type:List[PropertyAnimation]

    def __allAnins(self)->List[PropertyAnimation]:
        return self.__anis

    def setStartMode(self,mode:AnimationGroup):
        if Animation.Parallel == mode:
            self.__startMode = ParallelAnimationGroup()
        elif Animation.Sequential == mode:
            self.__startMode = SequentialAnimationGroup()
        else:
            raise Exception("No such mode!")

    def startMode(self)->AnimationGroup:
        return self.__startMode

    def addAni(self,
               sv:Any,ev:Any,
               atv:Union[List[Any],List[Tuple[float,Any]]]=None,
               targetObj = None,
               duration:int = 1200,
               propertyName:bytes = b"",
               selector:str = None,
               courseFunc:Callable = None,
               finishedCall:Callable = None,
               **kwargs):
        if targetObj and propertyName:
            ani = PropertyAnimation()
            ani.setTargetObject(targetObj)
            ani.setPropertyName(propertyName)
            if selector:
                ani.setSelector(selector)
        elif targetObj and courseFunc:
            ani = PropertyAnimation()
            ani.setTargetObject(targetObj)
            ani.courseFunc(courseFunc)
        elif targetObj:
            ani = PropertyAnimation()
            ani.setTargetObject(targetObj)
        elif courseFunc:
            ani = PropertyAnimation()
            ani.courseFunc(courseFunc)
        else:
            raise Exception('''
            Parameter passing error, when there is targetObj, targetObj and propertyName must be valid at the same time, 
            or targetObj and courseFunc must be valid at the same time, or, when there is no targetObj, 
            courseFunc is a required parameter.
            ''')

        if atv:ani.setStartEndValue(sv,ev,atv)
        else:ani.setStartEndValue(sv, ev)

        ani.setDuration(duration)
        if finishedCall:
            ani.finishedCall(finishedCall)
        self.__anis.append(ani)

    def start(self):
        group = self.startMode()
        group.addAnimations(self.__allAnins())
        group.start()

import re

s = "221px22"
print()