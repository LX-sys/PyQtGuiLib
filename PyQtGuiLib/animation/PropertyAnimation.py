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
    QColor,
    QSize,
    QPoint
)
import re
import typing
from typing import Any,List,Tuple,Union

from PyQtGuiLib.styles import QssStyleAnalysis


def strToObj(v_str:str)->Union[QColor,Any]:
    v_str = v_str.lower().strip()

    if "rgb" in v_str or "rgba" in v_str:
        color_list = [int(i) for i in re.findall(r"[0-9]{1,3}", v_str)]
        return QColor(*color_list)
    elif "#" == v_str[0]:
        return QColor(v_str)
    elif "px" in v_str or "pt" in v_str:
        px_number = re.findall("^([0-9]*)px|^([0-9]*)pt",v_str)
        if px_number:
            if px_number[0][0]:return int(px_number[0][0])
            else:return int(px_number[0][1])



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

    # 在设置选择器的同时创建出qss对象
    def setSelector(self,selector:str,qssObj:QssStyleAnalysis=None):
        self.__selector = selector
        # ----在这里判断是否为QSS属性,如果_qss对象创建过,则直接使用已创建的
        if qssObj is None and self.__isQssPropertyName(self.propertyName()):
            self._qss = QssStyleAnalysis(self.targetObject())
            self._qss.setQSS(self.targetObject().styleSheet())
        else:
            self._qss = qssObj

    # 该方法用来检测_qss是否被创建过,存在则返回
    def qss(self) -> Union[QssStyleAnalysis,bool]:
        if hasattr(self,"_qss"):
            return self._qss
        return False

    def selector(self) -> str:
        return self.__selector

    # 判断 propertyName 是否为 QSS的属性
    def __isQssPropertyName(self,propertyName:bytes)->bool:
        propertyName = propertyName.data().decode()
        if self.targetObject() and self.selector():
            if propertyName not in ["pos","size","geometry","windowOpacity"]:
                return True
        return False

    def setPropertyName(self, propertyName):
        if isinstance(propertyName,str):
            propertyName = propertyName.encode()
        super().setPropertyName(propertyName)

    # 函数执行过程中调用的函数
    def courseFunc(self,call):
        self.__call = call

    def func(self) -> typing.Callable:
        return self.__call

    # 分析this处理返回
    def __analysisThis(self, value: str):
        '''
            对 this 的处理,为了保证this能正确的被处理,请确保设置过动画对象
        '''
        if not self.targetObject():
            return value

        if self.propertyName() == b"size":
            return self.targetObject().size()
        elif self.propertyName() == b"pos":
            return self.targetObject().pos()
        elif self.propertyName() == b"geometry":
            return self.targetObject().rect()
        elif self.propertyName() == b"windowOpacity":
            return self.targetObject().windowOpacity()

    # 处理QSS属性动画
    def __selectorAni(self,Any):
        selector = self._qss.selector(self.selector())
        propertyName = self.propertyName().data().decode()
        if selector.isAttr(propertyName):
            if isinstance(Any, int):
                value = "{}px".format(Any)
            elif isinstance(Any, QColor):
                value = "rgba({},{},{},{})".format(*Any.getRgb())
            self._qss.selector(self.selector()).updateAttr(propertyName, value)

    def updateCurrentValue(self, Any):
        if self.func():
            self.func()(Any)
        elif self.selector(): # 如果给了选择器,则可以视为QSS样式属性
            self.__selectorAni(Any)
        else:
            super().updateCurrentValue(Any)

    def setStartValue(self, value: typing.Any) -> None:
        if isinstance(value, str) and value.lower().strip() == "this":
            value = self.__analysisThis(value)
        elif isinstance(value,str):
            value = strToObj(value)
        super().setStartValue(value)

    def setEndValue(self, value: typing.Any) -> None:
        if isinstance(value, str):
            value = strToObj(value)
        super().setEndValue(value)

    # 动画执行完成的回调函数
    def finishedCall(self,call):
        self.finished.connect(call)

    def valueChanged(self, Any):
        super().valueChanged(Any)

# ===================================================


class ParallelAnimationGroup(QParallelAnimationGroup):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def build(self,ani):
        if isinstance(ani.startMode(),ParallelAnimationGroup):
            group = QParallelAnimationGroup()
        else:
            group = QSequentialAnimationGroup()
        for ani in ani.allAnins():
            group.addAnimation(ani)
        self.addAnimation(group)

    def builds(self,anis:list):
        for ani in anis:
            self.build(ani)

    def addAnimations(self,anis:List[PropertyAnimation]):
        for ani in anis:
            self.addAnimation(ani)


class SequentialAnimationGroup(QSequentialAnimationGroup):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def addAnimations(self,anis:List[PropertyAnimation]):
        for ani in anis:
            self.addAnimation(ani)

    def build(self, ani):
        if isinstance(ani.startMode(), ParallelAnimationGroup):
            group = QParallelAnimationGroup()
        else:
            group = QSequentialAnimationGroup()
        for ani in ani.allAnins():
            group.addAnimation(ani)
        self.addAnimation(group)

    def builds(self,anis:list):
        for ani in anis:
            self.build(ani)