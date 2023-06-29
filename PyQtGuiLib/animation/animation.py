# -*- coding:utf-8 -*-
# @time:2023/4/198:53
# @author:LX
# @file:animation.py
# @software:PyCharm
from PyQtGuiLib.header import (
    QEasingCurve
)
from typing import Callable,Any,TypeVar,List,Union,Tuple
from PyQtGuiLib.animation.PropertyAnimation import ParallelAnimationGroup,SequentialAnimationGroup,PropertyAnimation


AnimationGroup = TypeVar("AnimationGroup",ParallelAnimationGroup,SequentialAnimationGroup)
'''
    动画框架重写
'''


class Animation:
    Parallel = 1
    Sequential = 2

    STOP = 0
    PAUSE = 1
    START = 2

    def __init__(self,):
        self.__startMode = SequentialAnimationGroup()  # 默认串行
        self.__anis = []  # type:List[PropertyAnimation]
        self.isBuilt = False

    def allAnins(self)->List[PropertyAnimation]:
        return self.__anis

    def setStartMode(self,mode:AnimationGroup):
        if Animation.Parallel == mode:
            self.__startMode = ParallelAnimationGroup()
        elif Animation.Sequential == mode:
            self.__startMode = SequentialAnimationGroup()
        else:
            raise Exception("No such mode!")

    def startMode(self) -> int:
        if isinstance(self.__startMode,SequentialAnimationGroup):
            return Animation.Sequential
        else:
            return Animation.Parallel

    def startModeObj(self)->AnimationGroup:
        return self.__startMode

    def addAni(self,
               sv:Any,ev:Any,
               atv:Union[List[Any],List[Tuple[float,Any]]]=None,
               targetObj = None,
               duration:int = 1200,
               propertyName:bytes = b"",
               loopCount:int = 1,
               easingCurve:QEasingCurve = None,
               selector:str = None,
               courseFunc:Callable = None,
               finishedCall:Callable = None,
               **kwargs):
        '''


        :param sv:
        :param ev:
        :param atv:
        :param targetObj:
        :param duration:
        :param propertyName:
        :param loopCount:
        :param easingCurve:
        :param selector: QSS选择器,注意:如果不是为了样式的动画,请不要设置该属性,避免多余的内存开销
        :param courseFunc:
        :param finishedCall:
        :param kwargs:
        :return:
        '''
        if targetObj and propertyName:
            ani = PropertyAnimation()
            ani.setTargetObject(targetObj)
            if selector:
                # 这一段保证了,多个QSS被修改时,最终的结果是一致的
                obj = self.findTargetObject(targetObj)
                if obj:
                    qss = obj.qss()
                    if qss:ani.setSelector(selector,qss)
                    else:ani.setSelector(selector)
                else:
                    ani.setSelector(selector)
            ani.setPropertyName(propertyName)
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

        if easingCurve:
            ani.setEasingCurve(easingCurve)

        ani.setDuration(duration)
        ani.setLoopCount(loopCount)
        if finishedCall:
            ani.finishedCall(finishedCall)
        self.__anis.append(ani)

    def addSeriesAni(self,
                     sv: Any, ev: Any,evs:List[Any],
                     atv: Union[List[Any], List[Tuple[float, Any]]] = None,
                     targetObj = None,
                     duration: int = 1200,
                     propertyName: bytes = b"",
                     loopCount: int = 1,
                     easingCurve: QEasingCurve = None,
                     selector: str = None,
                     courseFunc: Callable = None,
                     finishedCall: Callable = None,
                     **kwargs):
        '''

            使用该该函数必须将使用 setStartMode()将动画模式设置为串型(默认也是串型)

        :param sv:
        :param ev:
        :param evs: 连续变化值列表(必须是同一类型)
        :param atv:
        :param targetObj:
        :param duration:
        :param propertyName:
        :param loopCount:
        :param easingCurve:
        :param selector:
        :param courseFunc:
        :param finishedCall:
        :param kwargs:
        :return:
        '''
        if self.startMode() != Animation.Sequential:
            raise Exception("Sequential Animation is \"Animation.Sequential\" mode.")

        if not evs:
            raise Exception("The \"evs\" continuous change item should not be empty!")

        # 首先创建第一个动画
        self.addAni(sv,ev,atv,targetObj,duration,propertyName,
                    loopCount,easingCurve,selector,courseFunc,None,**kwargs)

        first_value = ev
        two_value = None

        for _ev in evs[:-1]:
            two_value = _ev
            self.addAni(first_value, two_value, atv, targetObj, duration, propertyName,
                        loopCount, easingCurve, selector, courseFunc, None, **kwargs)
            first_value = two_value

        if finishedCall:
            self.addAni(evs[-2], evs[-1],atv,targetObj,duration,propertyName,
                        loopCount,easingCurve,selector,courseFunc,finishedCall,**kwargs)
        else:
            self.addAni(evs[-2], evs[-1], atv, targetObj, duration, propertyName,
                        loopCount, easingCurve, selector, courseFunc, None, **kwargs)

    # 查找一个控件对象
    def findTargetObject(self,targetObj:Any)->Union[PropertyAnimation,None]:
        for obj in self.__anis:
            if targetObj is obj.targetObject():
                return obj
        return None

    def builtAni(self):
        # 该方法只会生效一次
        if not self.isBuilt:
            self.startModeObj().addAnimations(self.allAnins())
            self.isBuilt = True

    def start(self,isBuilt:bool=True):
        if isBuilt:
            self.builtAni()
        if not self.startModeObj().state():
            self.startModeObj().start()

    def state(self) -> int:
        return self.startModeObj().state()

    def resume(self):
        self.startModeObj().resume()

    def paused(self):
        self.startModeObj().pause()

    def stop(self):
        self.startModeObj().stop()