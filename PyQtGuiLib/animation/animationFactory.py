
from PyQtGuiLib.header import (
    QPropertyAnimation,
    QObject,
    QColor,
    QRect,
    QPoint,
    QSize,
    pyqtProperty,
    Signal

)
from PyQtGuiLib.styles import QssStyleAnalysis
from PyQtGuiLib.animation.animationDrawType import AniNumber


# 公用动画基类
class PropertyAnimation(QPropertyAnimation):
    drawfinished = Signal()

    Parallel = 1
    Sequential = 2
    # 动画对象模式
    Control = "control"  # 动画作用在普通控件上面
    Draw = "draw"  # 动画作用在绘制的图形上面

    def __init__(self,parent:QObject,ani_data:dict,ani_obj_mode="control"):
        self.__parent = parent
        super().__init__(parent)

        # 动画对象模式
        self.__ani_obj_mode = ani_obj_mode

        self.__all_ani_data = ani_data

        self.targetObj = ani_data.get("targetObj", None)
        self.propertyName = ani_data.get("propertyName", None)
        self.sv = ani_data.get("sv", None)
        self.atv = ani_data.get("atv", None)
        self.ev = ani_data.get("ev", None)
        self.call = ani_data.get("call", None)
        self.call_argc = ani_data.get("argc", None)
        self.selector = ani_data.get("selector", None)
        self.qssSuffix = ani_data.get("qss-suffix","px")

        self.duration = ani_data.get("duration", self.duration())
        self.special = ani_data.get("special", self.special())
        self.loopCount = ani_data.get("loop", self.loopCount())

        self.setTargetObject(self.targetObj)
        self.setDuration(self.duration)
        self.setSpecial(self.special)
        self.setLoopCount(self.loopCount)

        # 保存绘图动画的开始对象
        self.__drawStartObj = self.sv

    def drawSv(self):
        return self.__drawStartObj

    def allAniDatas(self)->dict:
        return self.__all_ani_data

    def aniObjMode(self):
        return self.__ani_obj_mode

    # 设置动效
    def setSpecial(self,special):
        self.setEasingCurve(special)

    def special(self):
        return self.easingCurve()

    # 刷新绘图动画
    def updateDraw(self):
        self.__parent.update()

    # 子类重写(默认模式)
    def createAni(self):
        self.setStartValue(self.sv)
        if self.atv:
            one_e = self.atv[0]
            if isinstance(one_e, tuple) or isinstance(one_e, list):
                for step, value in self.atv:
                    self.setKeyValueAt(step, value)
            else:
                mean_time = 1 / len(self.atv)  # 平均时间
                step = 0.0
                for value in self.atv:
                    step += mean_time
                    self.setKeyValueAt(step, value)
        self.setEndValue(self.ev)

        self.aniCall()

    # 执行动画的回调函数
    def aniCall(self):
        if self.call:
            if self.call_argc:
                self.finished.connect(lambda: self.call(self.targetObj, *self.call_argc))
            else:
                self.finished.connect(lambda: self.call(self.targetObj))


# 与QSS属性动画相关的基类
class QSSPropertyAnimation(PropertyAnimation):
    def __init__(self,parent:QObject,ani_data:dict,ani_obj_mode="control"):
        super().__init__(parent,ani_data,ani_obj_mode)

        if self.selector is None:
            raise Exception("backgroundColor The selector must be provided!")

        self.setPropertyName(self.propertyName)

        self.qss = QssStyleAnalysis(self.targetObj)
        self.qss.setQSS(self.targetObj.styleSheet())
        self.createAni()

    def updateState(self, newState, oldState) -> None:
        super().updateState(newState,oldState)

    def interpolated(self, from_, to, progress: float):
        return super().interpolated(from_,to,progress)

    def __toValue(self,value):
        if isinstance(value, int):
            value = "{}{}".format(value,self.qssSuffix)
        elif isinstance(value, QColor):
            value = value.name()
        else:
            raise Exception("This type is not supported yet.{}".format(value))
        return value

    def updateCurrentValue(self, value) -> None:
        self.qss.appendQSS(self.targetObj.styleSheet())
        self.qss.selector(self.selector).updateAttr(self.propertyName.decode(), self.__toValue(value))
        super().updateCurrentValue(value)

# --------------


# 通用普通控件动画
class AnimationControl(PropertyAnimation):
    def __init__(self,parent:QObject,ani_data:dict,ani_obj_mode="control"):
        super().__init__(parent,ani_data,ani_obj_mode)

        self.setPropertyName(self.propertyName)
        self.createAni()


# 普通绘图 - 单值动画
class AnimationDrawValue(PropertyAnimation):
    def __init__(self,parent:QObject,ani_data:dict,ani_obj_mode="control"):
        super().__init__(parent,ani_data,ani_obj_mode)

        self.setPropertyName(b"value")
        self.createAni()

    def setStartValue(self, value) -> None:
        if isinstance(value,int):
            super().setStartValue(value)
        elif isinstance(value,AniNumber):
            super().setStartValue(value.number())

    def updateState(self, newState, oldState) -> None:
        super().updateState(newState, oldState)

    def updateCurrentValue(self, value) -> None:
        if self.drawSv():
            self.drawSv().setNumber(value)
            self.updateDraw()



'''
    动画工厂
'''
class AnimationFactory:
    # 动画对象模式
    Control = "control"  # 动画作用在普通控件上面
    Draw = "draw"        # 动画作用在绘制的图形上面

    def __init__(self,parent,ani_data:dict,ani_obj_mode):
        self.__ani_data = ani_data
        self.__parent = parent
        self.__ani_obj_mode = ani_obj_mode

    def parent(self):
        return self.__parent

    def aniData(self) -> dict:
        return self.__ani_data

    def propertyName(self)->str:
        return self.__ani_data['propertyName']

    def aniObjMode(self):
        return self.__ani_obj_mode

    def argc(self) -> tuple:
        return self.parent(),self.aniData(),self.aniObjMode()

    # 返回动画的实例
    def createAni(self) -> QPropertyAnimation:
        if self.aniObjMode() == AnimationFactory.Control:
            if self.propertyName() in [b"geometry",b"size",b"pos",b"windowOpacity"]:
                ani = AnimationControl(*self.argc())
            elif self.propertyName() and self.aniData().get("selector",None):  # 处理所有qss属性
                ani = QSSPropertyAnimation(*self.argc())
            else:
                raise Exception("There is no animation property,{}!".format(self.propertyName()))
        elif self.aniObjMode() == AnimationFactory.Draw:
            if self.propertyName() == b"geometry":
                pass
            elif self.propertyName() == b"value":
                ani = AnimationDrawValue(*self.argc())
            else:
                raise Exception("There is no animation property!")
        else:
            raise Exception("This animation mode is not available!")

        return ani