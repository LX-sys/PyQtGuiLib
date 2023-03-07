# -*- coding:utf-8 -*-
# @time:2022/12/1211:41
# @author:LX
# @file:animation.py
# @software:PyCharm

from PyQtGuiLib.header import (
    sys,
    QApplication,
    QPropertyAnimation,
    QParallelAnimationGroup,
    QSequentialAnimationGroup,
    QWidget,
    QPushButton,
    QObject,
    qt
)

'''
    封装动画类
'''


class Animation:
    Parallel = 1
    Sequential = 2

    # 动效
    InCurve = qt.InCurve
    OutBounce = qt.OutBounce
    CosineCurve = qt.CosineCurve
    SineCurve = qt.SineCurve

    def __init__(self,parent=None):

        if parent:
            self.__parent = parent  # type:QObject
        else:
            self.__parent = None # type:QObject

        # 动画列表
        self.ani_list = []

        # 默认动画模式(并行)
        self.ani_mode = Animation.Parallel
        # 默认动画时长
        self.ani_duration = 1000
        # 默认动效
        self.ani_special = Animation.InCurve
        # 默认动画循环次数
        self.ani_loopCount = 1

        # 当前动画组对象
        self.ani_group_obj = None  # type:QParallelAnimationGroup

    def setParent(self,parent):
        self.__parent = parent

    def parent(self) -> QObject:
        return self.__parent

    def isParent(self)->bool:
        return bool(self.__parent)

    def special(self):
        return self.ani_special

    def loopCount(self)->int:
        return self.ani_loopCount

    def addAni(self,ani_data:dict):
        '''
        {
            "targetObj":xx
            "propertyName":""
            "duration":1000,  # 可不传该参数
            "special":        # 可不传该参数
            "loop":1          # 可不传该参数
            "call":fun  回调函数  # 可不传该参数
            "argc":tuple    回调函数的参数  # 可不传该参数
            "sv":xx
            "atv":[]          # 可不传该参数
            "ev":xx
        }
        最简化版
        {
            "targetObj":xx,
            "propertyName":"",
            "sv":xx,
            "ev":xx
        }
        :param ani_data:
        :return:
        '''
        targetObj = ani_data.get("targetObj",None)
        propertyName = ani_data.get("propertyName",None)
        duration = ani_data.get("duration",self.ani_duration)
        special = ani_data.get("special",self.special())
        loopCount = ani_data.get("loop",self.loopCount())
        sv = ani_data.get("sv",None)
        atv = ani_data.get("atv",None)
        ev = ani_data.get("ev",None)
        call = ani_data.get("call",None)
        call_argc = ani_data.get("argc",None)

        ani_ = QPropertyAnimation()

        if self.isParent() :
            ani_.setParent(self.parent())
        ani_.setPropertyName(propertyName)

        ani_.setEasingCurve(special)
        ani_.setLoopCount(loopCount)
        ani_.setTargetObject(targetObj)
        ani_.setDuration(duration)

        ani_.setStartValue(sv)
        if atv:
            for step,value in atv:
                ani_.setKeyValueAt(step,value)
        ani_.setEndValue(ev)

        if call:
            if call_argc:
                ani_.finished.connect(lambda :call(targetObj,*call_argc))
            else:
                ani_.finished.connect(lambda :call(targetObj))

        self.ani_list.append(ani_)

    def count(self) -> int:
        return len(self.ani_list)

    def removeAni(self,obj:QObject):
        '''
            在移除动画之前,需要先暂停
        :param obj:
        :return:
        '''

    def pause(self):
        if self.ani_group_obj:
            self.ani_group_obj.pause()

    def start(self):

        if self.ani_mode == Animation.Parallel:
            self.ani_group_obj = QParallelAnimationGroup(self.parent())
        if self.ani_mode == Animation.Sequential:
            self.ani_group_obj = QSequentialAnimationGroup(self.parent())

        for ani in self.ani_list:
            self.ani_group_obj.addAnimation(ani)
        self.ani_group_obj.start()

