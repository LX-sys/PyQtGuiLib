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
    qt,
    Signal,
    QRect
)

'''
    封装动画类
'''
from _ctypes import PyObj_FromPtr
import copy
from PyQtGuiLib.styles import QssStyleAnalysis

EA = 1

# 动画元素类(是一个完整独立的动画对象)
class AnimationElement(QPropertyAnimation):
    # 动画对象模式
    Control = "control"  # 动画作用在普通控件上面
    Draw = "draw"        # 动画作用在绘制的图形上面

    # 绘图动画执行完成的信号
    drawfinished = Signal()

    def __init__(self,parent:QObject,ani_data:dict,qss:QssStyleAnalysis=None,ani_obj_mode="control"):
        self.__parent = parent
        super().__init__(parent)

        # 动画对象模式
        self.__ani_obj_mode = ani_obj_mode

        print("AnimationElement --> ani_data:",id(ani_data),id(ani_data["sv"]))
        # 信息
        self.__ani_all_info = ani_data

        # 创建动画
        self.createAni(ani_data)

        '''
            如果当多个动画同时作用在一个目标上,
            则共享一个qss对象
        '''
        if self.__ani_obj_mode == AnimationElement.Control:
            if qss is None:
                self.__qss = QssStyleAnalysis(self.targetObject())
                self.__qss.setQSS(self.targetObject().styleSheet())
            else:
                self.__qss = qss

    def aniObjMode(self)->str:
        return self.__ani_obj_mode

    # 设置动效
    def setSpecial(self,special):
        self.setEasingCurve(special)

    def special(self):
        return self.easingCurve()

    def qss(self) -> QssStyleAnalysis:
        return self.__qss

    def __customPropertyAnimation(self,propertyName,selector):
        call_f = None

        if propertyName == b"backgroundColor":
            def __backgroundColor(color):
                self.qss().selector(selector).updateAttr("background-color", color.name())
            call_f = __backgroundColor
        elif propertyName == b"fontSize":
            def __fontSize(size):
                self.qss().selector(selector).updateAttr("font-size", "{}px".format(size))
            call_f = __fontSize
        elif propertyName == b"borderRadius":
            def __radius(r):
                self.qss().selector(selector).updateAttr("border-radius", "{}px".format(r))
            call_f = __radius

        if call_f:
            self.valueChanged.connect(call_f)

    def __customPropertyAnimationDraw(self,propertyName):
        sv = self.allInfo()["sv"] # 这一步获取绘制图形的开始数据
        self.setStartValue(sv)
        ev = self.allInfo()["ev"] # 获取结束值,作为发射信号的时机
        call_f = None

        if propertyName == b"geometry":
            def __drawGeometry(geometry):
                # print(geometry)
                sv.setX(geometry.x())
                sv.setY(geometry.y())
                sv.setWidth(geometry.width())
                sv.setHeight(geometry.height())
                self.__parent.repaint()
                if ev == geometry:
                    self.setStartValue(self.allInfo()["sv"])
                    print("结束sv:",)
                    self.drawfinished.emit()
            call_f = __drawGeometry

        self.valueChanged.connect(call_f)

    def allInfo(self) -> dict:
        return self.__ani_all_info

    def createAni(self,ani_data:dict):
        if not ani_data:
            return
        '''
        {
            "targetObj":xx
            "propertyName":""
            "duration":1000,  # 可不传该参数
            "special":        # 可不传该参数
            "loop":1          # 可不传该参数
            "call":fun  回调函数,这个回调函数必须有一个参数来接收系统的  # 可不传该参数
            "argc":tuple    回调函数的参数  # 可不传该参数
            "sv":xx
            "atv":[()] 或者 []          # 可不传该参数
            "ev":xx
            "selector":""  选择器,这个参数一般配合样式修改时使用 eg:backgroundColor # 可不传该参数
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
        targetObj = ani_data.get("targetObj", None)
        propertyName = ani_data.get("propertyName", None)
        sv = ani_data.get("sv", None)
        # 假设法
        global EA
        if EA == 0:
            print("dsa")
            sv.setRect(300, 200, 50, 200)
        else:
            EA= 0
        atv = ani_data.get("atv", None)
        ev = ani_data.get("ev", None)
        call = ani_data.get("call", None)
        call_argc = ani_data.get("argc", None)
        selector = ani_data.get("selector",None)
        duration = ani_data.get("duration",self.duration())
        special = ani_data.get("special",self.special())
        loopCount = ani_data.get("loop",self.loopCount())

        self.setTargetObject(targetObj)
        self.setPropertyName(propertyName)
        self.setDuration(duration)
        self.setSpecial(special)
        self.setLoopCount(loopCount)

        self.setStartValue(sv)
        if atv:
            one_e = atv[0]
            if isinstance(one_e,tuple) or isinstance(one_e,list):
                for step, value in atv:
                    self.setKeyValueAt(step, value)
            else:
                mean_time = 1/len(atv)  # 平均时间
                step = 0.0
                for value in atv:
                    mean_time += mean_time
                    self.setKeyValueAt(step, value)
        self.setEndValue(ev)

        # --------自定义动画
        if self.aniObjMode() == AnimationElement.Control and selector:
            self.__customPropertyAnimation(propertyName,selector)
        elif self.aniObjMode() == AnimationElement.Draw:
            self.__customPropertyAnimationDraw(propertyName)

        if call:
            if self.aniObjMode() == AnimationElement.Control:
                if call_argc:
                    self.finished.connect(lambda :call(targetObj,*call_argc))
                else:
                    self.finished.connect(lambda :call(targetObj))
            elif self.aniObjMode() == AnimationElement.Draw:
                if call_argc:
                    self.drawfinished.connect(lambda :call(targetObj,*call_argc))
                else:
                    self.drawfinished.connect(lambda :call(targetObj))


class Animation:
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
        '''
        控件动画
            目前动画支持的属性
            geometry
            pos
            size
            windowOpacity

            ---下面是对QSS属性的动画,使用动画的前提是qss里面必须有该属性
            backgroundColor ---> background-color  动画参数类型是 QColor
            fontSize  --> font-size                动画参数类型是 int
            borderRadius  --> border-radius        动画参数类型是 int
            -----end QSS

        绘图动画
            geometry 数类型 QRect 注意参数是QRect时


        :param parent: 如果这个参数不传递,则默认绘图动画模式
        :param mode
        '''

        if parent:
            self.__parent = parent  # type:QObject
        else:
            if ani_obj_mode == Animation.Draw:
                self.__parent = QObject()
            else:
                self.__parent = None # type:QObject

        # 动画对象模式
        self.__ani_obj_mode = ani_obj_mode

        # 动画列表(里面每一个元素都是一个完整的动画对象)
        self.ani_list = []
        # 目标对象列表
        self.targetObject_list = []

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

    def aniObjMode(self)->str:
        return self.__ani_obj_mode

    def setParent(self,parent):
        self.__parent = parent

    def setAniMode(self,mode):
        self.ani_mode = mode

    # 设置全局的动画时长
    def setDuration(self,duration):
        self.ani_duration = duration

    # 设置全局的动效
    def setSpecial(self,special):
        self.ani_special = special

    # 设置全局的动画循环次数
    def setLoopCount(self, count):
        self.ani_loopCount = count

    def parent(self) -> QObject:
        return self.__parent

    def isParent(self) -> bool:
        return bool(self.__parent)

    def duration(self) -> int:
        return self.ani_duration

    def special(self):
        return self.ani_special

    def loopCount(self) -> int:
        return self.ani_loopCount

    def aniObj(self) -> QParallelAnimationGroup:
        return self.ani_group_obj

    # 添加独立动画
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
            "atv":[()] 或者 []          # 可不传该参数
            "ev":xx
            "selector":""  选择器,这个参数一般配合修改样式时使用 eg:backgroundColor   # 可不传该参数
        }
        注意 sv,atv,ev 中的值的参数类型必须一致
        这里的每一个动画都是独立的,不会在并联动画连续播放
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
        targetObject = ani_data.get("targetObj", None)
        if self.aniObj() == Animation.Control and targetObject is None:
            raise Exception("No target object!")

        if self.aniObjMode() == Animation.Draw:
            ani_data["targetObj"] = QObject()
            # 绘图动画时,self.parent() 返回值一定 QObject()
            ani_ = AnimationElement(self.parent(), ani_data, None, self.aniObjMode())
        elif self.isParent():
            duration = ani_data.get("duration", None)
            special = ani_data.get("special", None)
            loopCount = ani_data.get("loop", None)

            if duration is None:
                ani_data["duration"] = self.duration()
            if special is None:
                ani_data["special"] = self.special()
            if loopCount is None:
                ani_data["loopCount"] = self.loopCount()

            one_ani = self.getOneAni(targetObject)

            if one_ani:
                ani_ = AnimationElement(self.parent(), ani_data,one_ani.qss())
            else:
                ani_ = AnimationElement(self.parent(),ani_data)
        else:
            raise Exception("There is no parent object.")

        self.ani_list.append(ani_)
        self.targetObject_list.append(ani_.targetObject())

    # 添加连续动画(运动必须是相同的)
    def addSeriesAni(self,ani_data:dict,variation:list):
        '''

        :param ani_data:
        :return:
        '''
        if self.ani_mode != Animation.Sequential:
            raise Exception("Current animation mode is not Animation.Sequential")

        first_ani = ani_data
        first_ev = first_ani["ev"] # 第一个动画的结尾作为下一个动画的开始
        # 获取回调函数
        call = first_ani.get("call",None)
        argc = first_ani.get("argc",None)
        if call:
            del first_ani["call"]
            first_ani["argc"] = None

        ani_list = [first_ani]
        for ev in variation:
            if self.aniObjMode() == Animation.Control:
                # 复制动画
                copy_ani = copy.copy(first_ani)
                copy_ani["sv"] = copy.deepcopy(first_ev)
                copy_ani["ev"] = copy.deepcopy(ev)
                first_ev = ev
            elif self.aniObjMode() == Animation.Draw:
                copy_ani = copy.deepcopy(first_ani)
                copy_ani["sv"] = ani_data["sv"]
                copy_ani["ev"] = ev
            ani_list.append(copy_ani)

        if call:
            end_ani = ani_list[-1]
            if argc:
                end_ani["call"] = call
                end_ani["argc"] = argc

        for ani in ani_list:
            self.addAni(ani)


    def count(self) -> int:
        return len(self.ani_list)

    # 根据目标对象来返回与这个对象相关的第一个动画
    def getOneAni(self, targetObject:QObject) -> AnimationElement:
        for obj in self.ani_list:
            if obj.targetObject() == targetObject:
                return obj
        return None

    # 根据目标对象来获取于这个目标相关的所有动画
    def getAllAni(self,targetObject:QObject) -> [AnimationElement]:
        obj_list = []
        for obj in self.ani_list:
            if obj.targetObject() == targetObject:
                obj_list.append(obj)
        return obj_list if obj_list else None

    def removeAni(self,obj:QObject):
        '''
            在移除动画之前,需要先暂停
        :param obj:
        :return:
        '''

    def pause(self,call=None,argc=None):
        if self.aniObj():
            self.aniObj().pause()

            if call:
                if argc:
                    call(*argc)
                else:
                    call()

    def resume(self,call=None,argc=None):
        if self.aniObj():
            self.aniObj().resume()

            if call:
                if argc:
                    call(*argc)
                else:
                    call()

    def state(self):
        if self.aniObj():
            if self.aniObj().state() == self.ani_group_obj.Running:
                return self.aniObj().Running
            if self.aniObj() == self.ani_group_obj.Paused:
                return self.aniObj().Paused
        else:
            return None

    # 开关
    def aniSwitch(self,btn:QPushButton=None,texts:dict=dict()):
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
        if self.aniObj():
            pause_ = texts.get("pause", "pause")
            resume_ = texts.get("resume", "resume")

            if self.aniObj().state() == self.aniObj().Running:
                self.pause()
                if btn:
                    btn.setText(resume_)
            elif self.aniObj().state() == self.aniObj().Paused:
                self.resume()
                if btn:
                    btn.setText(pause_)

    def start(self):
        if self.ani_mode == Animation.Parallel:
            self.ani_group_obj = QParallelAnimationGroup(self.parent())
        if self.ani_mode == Animation.Sequential:
            self.ani_group_obj = QSequentialAnimationGroup(self.parent())

        for ani in self.ani_list:
            self.aniObj().addAnimation(ani)

        self.aniObj().start()

