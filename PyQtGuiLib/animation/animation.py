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
import pprint
from PyQtGuiLib.animation.animationFactory import AnimationFactory,PropertyAnimation
from PyQtGuiLib.animation.animationDrawType import AniNumber,AniNumbers,AniColor,AniRect,AniShadow

AniMode = int
ObjMode = str
AniStartType = TypeVar("AniStartType",AniNumber,AniNumbers,AniColor,AniRect)
AniEndType = TypeVar("AniEndType",list,QColor,QRect)
AnimationModeType = TypeVar("AnimationModeType",QParallelAnimationGroup,QSequentialAnimationGroup)


# 动画属性类
class AnimationAttr:
    '''

        并行模式
        串行模式
        混合模式
    '''
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
    '''

        主要方法:
            addAni()  最常用的添加单个动画的方式
            addAnis() 添加多个单个动画的方式
            addSeriesAni() 添加连续动画的方法
                - 连续动作必须一致,Eg: 初始动作是pos,那么后续动作也必须的pos
                - 这个方法必须最串行模式下运行

            addValuesAni() 多值动画,这个方法比较特殊
                - 使用这个方法之前,这个类的初始模式必须会绘图模式
            addBlend() 添加混合动画
                - 这个方法必须最串行模式下运行
                - 这个方法最好单独使用,不要和其他添加动画的方式一起使用
    '''
    BlendStart = AnimationAttr.Sequential
    BlendEnd = AnimationAttr.Parallel

    def __init__(self, parent: QObject = None, ani_obj_mode="control"):
        super(Animation, self).__init__(parent,ani_obj_mode)

        # 动画列表(里面每一个元素都是一个完整的动画对象)
        self.ani_list = []

        # 混合动画标记
        self._blendFlag = Animation.BlendEnd

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

    # 创建动画
    def __createAni(self,ani_data:dict)->PropertyAnimation:
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
             "comment":xx  # 备注  可选参数
             "blendFlag":True/False 混合动画标志,表示在混合模式下这类东西是串行的  可选参数
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
            ani = AnimationFactory(self.parent(), ani_data, self.aniObjMode()).createAni()
        elif self.isDrawMode():
            ani_data["targetObj"] = QObject()
            ani = AnimationFactory(self.parent(), ani_data, self.aniObjMode()).createAni()
        else:
            raise Exception("Pattern error,Only Animation.Control or Animation.Draw is supported!")
        return ani

    def addAni(self,ani_data:dict):
        self.ani_list.append(self.__createAni(ani_data))

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
            if i == variation_len-1:  # 这里判断是否是最后一项数值
                if Call: ani_data["call"] = Call
                if CallAgrc: ani_data["argc"] = CallAgrc
            ani_data["sv"] = sv
            ani_data["ev"] = ev
            e_ani = AnimationFactory(self.parent(), ani_data, self.aniObjMode()).createAni()
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

    # 添加混合动画
    def addBlend(self,ani_datas:list):
        '''
            混合模式必须的串行
            混合动画,专注处理,即需要并行的动画,由需要串行的动画
                    n个动画组成并行 --> n个动画组成串行 --> n个动画组成并行,...
            [
                {
                "targetObj": xxx,
                "propertyName": xxx,
                "sv": xxx,
                "ev": xxxx,
                },
                {
                "targetObj": xxx,
                "propertyName": xxx,
                "sv": xxx,
                "ev": xxxx,
                },
                {
                "targetObj": xxx,
                "propertyName": xxx,
                "sv": xxx,
                "ev": xxxx,
                "blendFlag":True
                },
                {
                "targetObj": xxx,
                "propertyName": xxx,
                "sv": xxx,
                "ev": xxxx,
                "blendFlag":True
                },
                ....
            ]
            这个参数 表示先执行一组 并行动画之后,在执行一组串行动画
        :return:
        '''
        if not ani_datas:
            return

        if self.aniMode() != Animation.Sequential:
            raise Exception("The blend mode must be Animation.Sequential")

        # 并行/串行动画列表
        ani_list = []

        '''
            根据第一个动画数据进行动画标记
        '''
        ani_flag = Animation.Sequential if ani_datas[0].get("blendFlag",False) else Animation.Parallel

        temp_list = []

        for data in ani_datas:
            if data.get("blendFlag",False) is False:
                if ani_flag == Animation.Sequential:
                    ani_list.append({"datas":temp_list,"aniMode":Animation.Sequential})
                    temp_list = []

                ani_flag = Animation.Parallel
            else:
                if ani_flag == Animation.Parallel:
                    ani_list.append({"datas":temp_list,"aniMode":Animation.Parallel})
                    temp_list = []

                ani_flag = Animation.Sequential
            temp_list.append(self.__createAni(data))

        if ani_flag == Animation.Sequential:
            ani_list.append({"datas":temp_list,"aniMode":Animation.Sequential})
        else:
            ani_list.append({"datas":temp_list,"aniMode":Animation.Parallel})

        # 混合
        blend_list = []
        for data in ani_list:
            data:dict
            aniMode, datas = data["aniMode"],data["datas"]

            if aniMode == Animation.Parallel:
                g_ani = QParallelAnimationGroup()
            else:
                g_ani = QSequentialAnimationGroup()

            for ani in datas:
                g_ani.addAnimation(ani)
            blend_list.append(g_ani)

        self._blendFlag = Animation.BlendStart # 混合模式开启
        self.setAniMode(Animation.BlendStart)
        for ani in blend_list:
            self.ani_list.append(ani)

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

        # 结束混合模式
        def _f():
            self.setAniMode(self._blendFlag)
            self.aniGroupObj().disconnect()


        if self._blendFlag == Animation.BlendStart:
            self._blendFlag = Animation.BlendEnd
            self.aniGroupObj().finished.connect(_f)

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

    def getAni(self,index:int)->PropertyAnimation:
        return self.ani_list[index]

    # 根据备注获取动画
    def getCommentAni(self,comment:str) -> PropertyAnimation:
        for ani in self.ani_list:
            if ani.commentInfo() == comment:
                return ani

    # 更新单个动画的信息
    def updateAni(self,ani:PropertyAnimation,new_datas:dict):
        ani.updateAni(new_datas)

    def removeAni(self,index:int):
        del self.ani_list[index]

    # 根据备注来移除动画
    def removeCommentAni(self,comment:str,count=1):
        '''

        :param comment:
        :param count: 默认只删除遇到的第一个相匹配的值,如果需要删除所有相匹配的值(count=-1)
        :return:
        '''
        temp_count = 0
        for ani in self.ani_list[::-1]:
            if count != -1 and (temp_count == count):
                break
            if ani.commentInfo() == comment:
                self.ani_list.remove(ani)
                temp_count += 1