from PyQtGuiLib.header import (
    QParallelAnimationGroup,
    QSequentialAnimationGroup,
    QPushButton,
    QObject,
    qt,
    QRect,
    QColor
)
from typing import TypeVar
from collections.abc import Callable
import copy
'''
    重构动画框架
    Animation 仅创建,管理,播放动画
'''

from PyQtGuiLib.animation.animationFactory import AnimationFactory
from PyQtGuiLib.animation.animationDrawType import AniNumber,AniNumbers,AniColor,AniRect,AniShadow

AniMode = int
ObjMode = str
AniStartType = TypeVar("AniStartType",AniNumber,AniNumbers,AniColor,AniRect)
AniEndType = TypeVar("AniEndType",list,QColor,QRect)
AnimationModeType = TypeVar("AnimationModeType",QParallelAnimationGroup,QSequentialAnimationGroup)


# 动画属性类
class AnimationAttr:
    Parallel = 1
    Sequential = 2

    # 动画对象模式
    Control = "control"  # 动画作用在普通控件上面
    Draw = "draw"        # 动画作用在绘制的图形上面

    # 动效
    InCurve = qt.InCurve
    OutBounce = qt.OutBounce
    CosineCurve = qt.CosineCurve
    SineCurve = qt.SineCurve

    def __init__(self,parent:QObject=None,ani_obj_mode="control"):
        self.__parent = None
        self.__ani_obj_mode = ani_obj_mode
        self.__ani_group_obj = None # 动画组对象

        # 默认动画模式(并行)
        self.__ani_mode = AnimationAttr.Parallel
        # 默认动画时长
        self.__ani_duration = 1000
        # 默认动效
        self.__ani_special = AnimationAttr.InCurve
        # 默认动画循环次数
        self.__ani_loopCount = 0

        if parent:
            self.setParent(parent)

    def setParent(self,parent):
        self.__parent = parent

    def setAniMode(self,mode:AniMode):
        self.__ani_mode = mode

    def setDuration(self,duration:int):
        self.__ani_duration = duration

    def setSpecial(self, special):
        self.__ani_special = special

    def setLoopCount(self, count:int):
        self.__ani_loopCount = count

    def setAniGroupObj(self,obj:AnimationModeType):
        if isinstance(obj,QParallelAnimationGroup) or isinstance(obj,QSequentialAnimationGroup):
            self.__ani_group_obj = obj
        else:
            raise Exception("Attribute error!")

    def parent(self) -> QObject:
        return self.__parent

    def aniMode(self) -> AniMode:
        return self.__ani_mode

    def duration(self) -> int:
        return self.__ani_duration

    def special(self):
        return self.__ani_special

    def loopCount(self) -> int:
        return self.__ani_loopCount

    def aniObjMode(self) -> ObjMode:
        return self.__ani_obj_mode

    def aniGroupObj(self) -> AnimationModeType:
        return self.__ani_group_obj

    def isAniGroupObj(self) -> bool:
        return True if self.aniGroupObj() else False

    def isControlMode(self) -> bool:
        return True if self.aniObjMode() == AnimationAttr.Control else False

    def isDrawMode(self) -> bool:
        return True if self.aniObjMode() == AnimationAttr.Draw else False

    # 绘图动画的 值封装
    @staticmethod
    def createAniNumber(value) -> AniNumber:
        return AniNumber(value)

    # 绘图动画的 多值封装
    @staticmethod
    def createAniNumbers(*args) -> AniNumbers:
        return AniNumbers(*args)

    # 绘图动画的 颜色值封装
    @staticmethod
    def createAniColor(*args) -> AniColor:
        return AniColor(*args)

    # 绘图动画的 矩形值封装
    @staticmethod
    def createAniRect(*args) -> AniRect:
        return AniRect(*args)

    # 绘图动画的 阴影封装
    @staticmethod
    def createAniShadow(*args) -> AniShadow:
        return AniShadow(*args)


# 动画类
class Animation(AnimationAttr):
    def __init__(self, parent: QObject = None, ani_obj_mode="control"):
        super(Animation, self).__init__(parent,ani_obj_mode)

        # 动画列表(里面每一个元素都是一个完整的动画对象)
        self.ani_list = []

    # 设置通用属性
    def __setGeneralAttr(self,ani_data:dict):
        duration = ani_data.get("duration", None)
        special = ani_data.get("special", None)
        loopCount = ani_data.get("loop", None)

        if duration is None:
            ani_data["duration"] = self.duration()
        if special is None:
            ani_data["special"] = self.special()
        if loopCount is None:
            ani_data["loopCount"] = self.loopCount()

    def addAni(self,ani_data:dict):
        '''
        {
            "targetObj":xx
            "propertyName":""
            "duration":1000,  # 可选参数
            "special":        # 可选参数
            "loop":1          # 可选参数
            "call":fun  回调函数  # 可选参数
            "argc":tuple    # 回调函数的参数  可选参数
            "sv":xx  # 该参数在控件模式下,可以写 this 指向自己的属性
            "atv":[()] 或者 []          # 可选参数
            "ev":xx
            "selector":""  # 选择器,这个参数qss样式动画时使用 eg:backgroundColor  可选参数
            "qss-suffix":"px"  # qss属性单位 如果: 写宽度时单位是px,表示文字大小时,有时候会用到pt  可选参数
            "isEffect":True/False # 这个参数觉得了是否开启特殊动画,阴影,模糊 可选参数
        }
        注意 sv,atv,ev 中的值的参数类型必须一致
        这里的每一个动画都是独立的,不会在并联动画连续播放
        普通控件动画最简化版
        {
            "targetObj":xx,
            "propertyName":"",
            "sv":xx,
            "ev":xx
        }
       绘图动画最简化版
        {
            "propertyName":"",
            "sv":xx,
            "ev":xx
        }
        :param ani_data:
        :return:
        '''
        if not ani_data:
            return

        self.__setGeneralAttr(ani_data)

        if self.isControlMode() and self.parent():
            ani = AnimationFactory(self.parent(),ani_data,self.aniObjMode()).createAni()
        elif self.isDrawMode():
            ani_data["targetObj"] = QObject()
            ani = AnimationFactory(self.parent(), ani_data, self.aniObjMode()).createAni()
        else:
            raise Exception("Pattern error,Only Animation.Control or Animation.Draw is supported!")

        self.ani_list.append(ani)

    def addAnis(self,*args):
        for ani_data in args:
            self.addAni(ani_data)

    # 添加连续动画(运动必须是相同的)
    def addSeriesAni(self, ani_data: dict, variation: list):
        '''
            连续动画是由单个具有相同的行为动画的组合
        :param ani_data:
        :param variation:
        :return:
        '''
        if not ani_data:
            return

        if self.aniMode() != Animation.Sequential:
            raise Exception("Current animation mode is not Animation.Sequential")

        if not self.isDrawMode() and not self.isControlMode():
            raise Exception("Pattern error,Only Animation.Control or Animation.Draw is supported!")

        if not self.parent():
            raise Exception("No superclass")

        self.__setGeneralAttr(ani_data)

        '''
                      如果有回调函数,保存之后,先移除掉,最后添加在末尾
                  '''
        Call = ani_data.get("call", None)
        CallAgrc = ani_data.get("argc", None)
        if Call: del ani_data["call"]
        if CallAgrc: del ani_data["argc"]

        # 首先创建出 初始动画
        ani = AnimationFactory(self.parent(), ani_data, self.aniObjMode()).createAni()
        self.ani_list.append(ani)
        sv = ani.endValue()

        if self.isDrawMode():
            ani_data["targetObj"] = QObject()

        # 在创建出后续的连续动画
        variation_len = len(variation)
        for i,ev in enumerate(variation):
            ev = variation[i]
            if i == variation_len-1:  # 这里判断是否是最后一项数值
                if Call: ani_data["call"] = Call
                if CallAgrc: ani_data["argc"] = CallAgrc
            ani_data["ev"] = ev
            e_ani = AnimationFactory(self.parent(), ani_data, self.aniObjMode()).createAni()
            e_ani.setStartValue(sv)
            e_ani.setEndValue(ev)
            sv = ev
            self.ani_list.append(e_ani)

    # 绘图-多值动画
    def addValuesAni(self,ani_data: dict,startObj:AniStartType,ends:AniEndType):
        '''


        :param ani_data:
        :param startObj: 参数类型 AniColor,AniNumbers
        :param ends:
        :return:
        '''
        # if self.isDrawMode():
        # 先移除属性


        Sv = ani_data.get("sv",None)
        Ev = ani_data.get("ev",None)
        Call = ani_data.get("call",None)
        if Sv:del ani_data["sv"]
        if Ev:del ani_data["ev"]
        if Call:del ani_data["call"]

        # 类型检测,并转换
        if isinstance(ends,QColor):
            ends = ends.getRgb()
        elif isinstance(ends,QRect):
            ends = ends.getRect()

        for sv,ev in zip(startObj.numberObjs(),ends):
            if self.isDrawMode():
                TargetObj = ani_data.get("targetObj")
                if TargetObj: del ani_data["targetObj"]
                copy_ani_data = copy.deepcopy(ani_data)
            else:
                copy_ani_data = copy.copy(ani_data)
            copy_ani_data["targetObj"] = copy_ani_data.get("targetObj",QObject())
            copy_ani_data["sv"] = sv
            copy_ani_data["ev"] = ev
            self.addAni(copy_ani_data)
    # else:
    #     raise Exception("addValuesAni() This method supports only the Animation.Draw mode!")

    # Executive function
    def __exeCall(self,call:Callable, argc=None):
        if call:
            if argc:
                call(*argc)
            else:
                call()

    def pause(self,call:Callable=None, argc=None):
        if self.isAniGroupObj():
            self.aniGroupObj().pause()
            self.__exeCall(call,argc)

    def resume(self,call:Callable=None,argc=None):
        if self.isAniGroupObj():
            self.aniGroupObj().resume()
            self.__exeCall(call,argc)

    def state(self):
        if self.isAniGroupObj():
            if self.aniGroupObj().state() == self.aniGroupObj().Running:
                return self.aniGroupObj().Running
            if self.aniGroupObj() == self.aniGroupObj().Paused:
                return self.aniGroupObj().Paused
        else:
            return None

    def start(self):
        if self.aniMode() == Animation.Parallel:
            self.setAniGroupObj(QParallelAnimationGroup(self.parent()))
        if self.aniMode() == Animation.Sequential:
            self.setAniGroupObj(QSequentialAnimationGroup(self.parent()))

        for ani in self.ani_list:
            self.aniGroupObj().addAnimation(ani)

        self.aniGroupObj().start()

    # 开关
    def aniSwitch(self,btn:QPushButton=None,texts:dict=None):
        '''
            动画开关
            如果动画当前状态是运行,则暂停,反之,运行
            __________________________________
            btn: 给定一个按钮(可选)
            texts:{
                "pause":"xxx",
                "resume":"xx"
            }
        :return:
        '''
        if texts is None:
            texts = dict()

        if self.isAniGroupObj():
            pause_ = texts.get("pause", "pause")
            resume_ = texts.get("resume", "resume")

            if self.aniGroupObj().state() == self.aniGroupObj().Running:
                self.pause()
                if btn:
                    btn.setText(resume_)
            elif self.aniGroupObj().state() == self.aniGroupObj().Paused:
                self.resume()
                if btn:
                    btn.setText(pause_)