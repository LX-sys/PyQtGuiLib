
from PyQtGuiLib.header import (
    QPropertyAnimation,
    QObject,
    QColor,
    QRect,
    QPoint,
    QSize,
    pyqtProperty,

)
from PyQtGuiLib.styles import QssStyleAnalysis


# 公用动画基类
class PropertyAnimation(QPropertyAnimation):
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
        self.duration = ani_data.get("duration", self.duration())
        self.special = ani_data.get("special", self.special())
        self.loopCount = ani_data.get("loop", self.loopCount())

        self.setTargetObject(self.targetObj)
        self.setDuration(self.duration)
        self.setSpecial(self.special)
        self.setLoopCount(self.loopCount)

    def allAniDatas(self)->dict:
        return self.__all_ani_data

    def aniObjMode(self):
        return self.__ani_obj_mode

    # 设置动效
    def setSpecial(self,special):
        self.setEasingCurve(special)

    def special(self):
        return self.easingCurve()

    # 子类重写(默认模式)
    def createAni(self):
        self.setStartValue(self.sv)
        if self.atv:
            one_e = self.atv[0]
            if isinstance(one_e, tuple) or isinstance(one_e, list):
                for step, value in atv:
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
            if self.aniObjMode() == AnimationGeometry.Control:
                if self.call_argc:
                    self.finished.connect(lambda: self.call(self.targetObj, *self.call_argc))
                else:
                    self.finished.connect(lambda: self.call(self.targetObj))
            elif self.aniObjMode() == AnimationGeometry.Draw:
                if self.call_argc:
                    self.drawfinished.connect(lambda: self.call(self.targetObj, *self.call_argc))
                else:
                    self.drawfinished.connect(lambda: self.call(self.targetObj))


# 与QSS属性动画相关的基类
class QSSPropertyAnimation(PropertyAnimation):
    def __init__(self,parent:QObject,ani_data:dict,ani_obj_mode="control"):
        super().__init__(parent,ani_data,ani_obj_mode)

        if self.selector is None:
            raise Exception("backgroundColor The selector must be provided!")

        self.qss = QssStyleAnalysis(self.targetObj)
        self.qss.setQSS(self.targetObj.styleSheet())

    def updateState(self, newState, oldState) -> None:
        super().updateState(newState,oldState)

    def updateCurrentValue(self, value) -> None:
        super().updateCurrentValue(value)

# --------------

# 普通控件动画 Geometry
class AnimationGeometry(PropertyAnimation):
    def __init__(self,parent:QObject,ani_data:dict,ani_obj_mode="control"):
        super().__init__(parent,ani_data,ani_obj_mode)

        self.setPropertyName(b"geometry")
        self.createAni()


# 普通控件动画 size
class AnimationSize(PropertyAnimation):
    def __init__(self,parent:QObject,ani_data:dict,ani_obj_mode="control"):
        super().__init__(parent,ani_data,ani_obj_mode)

        self.setPropertyName(b"size")
        self.createAni()


# 普通控件动画 pos
class AnimationPos(PropertyAnimation):
    def __init__(self,parent:QObject,ani_data:dict,ani_obj_mode="control"):
        super().__init__(parent,ani_data,ani_obj_mode)

        self.setPropertyName(b"pos")
        self.createAni()


# 控件属性动画 -qss - backgroundColor
class AnimationBackgroundColor(QSSPropertyAnimation):
    def __init__(self,parent:QObject,ani_data:dict,ani_obj_mode="control"):
        super().__init__(parent,ani_data,ani_obj_mode)

        self.setPropertyName(b"backgroundColor")
        self.createAni()

    def updateCurrentValue(self, value) -> None:
        self.qss.selector(self.selector).updateAttr("background-color",value.name())


# 控件属性动画 -qss - borderRadius
class AnimationBorderRadius(QSSPropertyAnimation):
    def __init__(self,parent:QObject,ani_data:dict,ani_obj_mode="control"):
        super().__init__(parent,ani_data,ani_obj_mode)

        self.setPropertyName(b"borderRadius")
        self.createAni()

    def updateCurrentValue(self, value) -> None:
        self.qss.selector(self.selector).updateAttr("border-radius","{}px".format(value))


# 控件属性动画 -qss - borderWidth
class AnimationBorderWidth(QSSPropertyAnimation):
    def __init__(self,parent:QObject,ani_data:dict,ani_obj_mode="control"):
        super().__init__(parent,ani_data,ani_obj_mode)

        self.setPropertyName(b"borderWidth")
        self.createAni()

    def updateCurrentValue(self, value) -> None:
        self.qss.selector(self.selector).updateAttr("border-width","{}px".format(value))


# 控件属性动画 -qss - borderColor
class AnimationBorderColor(QSSPropertyAnimation):
    def __init__(self,parent:QObject,ani_data:dict,ani_obj_mode="control"):
        super().__init__(parent,ani_data,ani_obj_mode)

        self.setPropertyName(b"borderColor")
        self.createAni()

    def updateCurrentValue(self, value) -> None:
        self.qss.selector(self.selector).updateAttr("border-color",value.name())


# 控件属性动画 -qss - fontSize
class AnimationFontSize(QSSPropertyAnimation):
    def __init__(self,parent:QObject,ani_data:dict,ani_obj_mode="control"):
        super().__init__(parent,ani_data,ani_obj_mode)

        self.setPropertyName(b"fontSize")
        self.createAni()

    def updateCurrentValue(self, value) -> None:
        self.qss.selector(self.selector).updateAttr("font-size","{}px".format(value))

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

    # 返回动画的实例
    def createAni(self) -> QPropertyAnimation:
        if self.aniObjMode() == AnimationFactory.Control:
            if self.propertyName() == b"geometry":
                ani = AnimationGeometry(self.parent(),self.aniData(),self.aniObjMode())
            elif self.propertyName() == b"size":
                ani = AnimationSize(self.parent(),self.aniData(),self.aniObjMode())
            elif self.propertyName() == b"pos":
                ani = AnimationPos(self.parent(),self.aniData(),self.aniObjMode())
            elif self.propertyName() == b"backgroundColor":
                ani = AnimationBackgroundColor(self.parent(),self.aniData(),self.aniObjMode())
            elif self.propertyName() == b"borderRadius":
                ani = AnimationBorderRadius(self.parent(),self.aniData(),self.aniObjMode())
            elif self.propertyName() == b"fontSize":
                ani = AnimationFontSize(self.parent(),self.aniData(),self.aniObjMode())
            elif self.propertyName() == b"borderWidth":
                ani = AnimationBorderWidth(self.parent(), self.aniData(), self.aniObjMode())
            elif self.propertyName() == b"borderColor":
                ani = AnimationBorderColor(self.parent(), self.aniData(), self.aniObjMode())
            else:
                raise Exception("There is no animation property,{}!".format(self.propertyName()))

        elif self.aniObjMode() == AnimationFactory.Draw:
            if self.propertyName() == b"geometry":
                pass
            else:
                raise Exception("There is no animation property!")
        else:
            raise Exception("This animation mode is not available!")

        return ani