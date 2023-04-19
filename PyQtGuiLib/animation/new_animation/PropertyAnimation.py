# -*- coding:utf-8 -*-
# @time:2023/4/1910:39
# @author:LX
# @file:PropertyAnimation.py
# @software:PyCharm
from PyQtGuiLib.header import (
    QPropertyAnimation,
    QParallelAnimationGroup,
    QSequentialAnimationGroup,
    QObject,
    QColor
)
import re
import typing
from typing import Any,List,TypeVar,Tuple,Union

from PyQtGuiLib.styles import QssStyleAnalysis

# 单个动画类
class PropertyAnimation(QPropertyAnimation):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.setTargetObject(QObject())
        self.setDuration(1200)

        self.__call = None
        self.__selector = None
    
    def setStartEndValue(self,sv:Any,ev:Any,atv:Union[List[Any],List[Tuple[float,Any]]]=None):
        self.setStartValue(sv)
        if atv:
            one_e = atv[0]
            if isinstance(one_e, tuple) or isinstance(one_e, list):
                for step, value in atv:
                    self.setKeyValueAt(step, value)
            else:
                mean_time = 1 / len(atv)  # 平均时间
                step = 0.0
                for value in atv:
                    step += mean_time
                    self.setKeyValueAt(step, value)
        self.setEndValue(ev)

    def setSelector(self,selector:str):
        self.__selector = selector

    def selector(self)->str:
        return self.__selector

    # 判断 propertyName 是否为 QSS的属性
    def __isQssPropertyName(self,propertyName:bytes)->bool:
        propertyName = propertyName.decode()
        return True

    def setPropertyName(self, propertyName):
        if isinstance(propertyName,str):
            propertyName = propertyName.encode()

        # ----在这里判断是否为QSS属性
        if self.__isQssPropertyName(propertyName):
            self.__qss = QssStyleAnalysis(self.targetObject())
            self.__qss.setQSS(self.targetObject().styleSheet())
        super().setPropertyName(propertyName)

    # 函数执行过程中调用的函数
    def courseFunc(self,call):
        self.__call = call

    def func(self) -> typing.Callable:
        return self.__call

    # 分析this处理返回
    def __analysisThis(self, value: str):
        if isinstance(value, str) and value.lower().strip() == "this":
            pass
        else:
            return value

    # 处理QSS属性动画
    def __selectorAni(self,Any):
        selector = self.__qss.selector(self.selector())
        propertyName = self.propertyName().data().decode()
        if selector.isAttr(propertyName):
            if isinstance(Any, int):
                value = "{}px".format(Any)
            elif isinstance(Any, QColor):
                value = "rgba({},{},{},{})".format(*Any.getRgb())
            self.__qss.selector(self.selector()).updateAttr(propertyName, value)

    def updateCurrentValue(self, Any):
        if self.func():
            self.func()(Any)
        elif self.selector(): # 如果给了选择器,则可以视为QSS样式属性
            self.__selectorAni(Any)
        else:
            super().updateCurrentValue(Any)

    def setStartValue(self, value: typing.Any) -> None:
        super().setStartValue(self.__analysisThis(value))

    # 动画执行完成的回调函数
    def finishedCall(self,call):
        self.finished.connect(call)

    def valueChanged(self, Any):
        super().valueChanged(Any)


class ParallelAnimationGroup(QParallelAnimationGroup):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def addAnimations(self,anis:List[PropertyAnimation]):
        for ani in anis:
            self.addAnimation(ani)


class SequentialAnimationGroup(QSequentialAnimationGroup):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def addAnimations(self,anis:List[PropertyAnimation]):
        for ani in anis:
            self.addAnimation(ani)