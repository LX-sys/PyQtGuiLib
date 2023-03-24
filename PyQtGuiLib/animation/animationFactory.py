import re
import typing
from PyQtGuiLib.header import (
    QPropertyAnimation,
    QObject,
    QColor,
    QRect,
    QPoint,
    QSize,
    pyqtProperty,
    Signal,
    QGraphicsDropShadowEffect,
    QGraphicsBlurEffect
)
from PyQtGuiLib.styles import QssStyleAnalysis
from PyQtGuiLib.animation.animationDrawType import AniNumber
'''
    QPropertyAnimation: you're trying to animate a non-existing property value of your QObject
    该警告出现mac下,部分win可能也会出现,可以忽略该警告
'''


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
        self.attr = ani_data["propertyName"].decode()
        super().__init__(parent)

        # 动画对象模式
        self.__ani_obj_mode = ani_obj_mode

        self.__all_ani_data = ani_data

        self.aniInit()

        # 保存绘图动画的开始对象
        self.__drawStartObj = self.sv

    def allAniDatas(self)->dict:
        return self.__all_ani_data

    def aniInit(self):
        self.targetObj = self.allAniDatas().get("targetObj", None)
        self.propertyName = self.allAniDatas().get("propertyName", None)
        self.sv = self.allAniDatas().get("sv", None)
        self.atv = self.allAniDatas().get("atv", None)
        self.ev = self.allAniDatas().get("ev", None)
        self.call = self.allAniDatas().get("call", None)
        self.call_argc = self.allAniDatas().get("argc", None)
        self.selector = self.allAniDatas().get("selector", None)
        self.qssSuffix = self.allAniDatas().get("qss-suffix", "px")

        special = self.allAniDatas().get("special", self.special())
        duration = self.allAniDatas().get("duration", self.duration())
        loopCount = self.allAniDatas().get("loop", self.loopCount())

        self.setTargetObject(self.targetObj)
        self.setDuration(duration)
        self.setSpecial(special)
        self.setLoopCount(loopCount)

    def drawSv(self):
        return self.__drawStartObj

    def aniObjMode(self):
        return self.__ani_obj_mode

    # 设置动效
    def setSpecial(self,special):
        self.setEasingCurve(special)

    def special(self):
        return self.easingCurve()

    # 判断sv是不是this
    def isThis(self) -> bool:
        if isinstance(self.sv,str) and self.sv.lower() == "this":
            return True
        return False

    # 判断是否开启特殊动画
    def isEffect(self) -> bool:
        return True if self.allAniDatas().get("isEffect",None) else False

    # 返回备注信息
    def commentInfo(self) -> str:
        return self.allAniDatas().get("comment","")

    # 刷新绘图动画
    def updateDraw(self):
        self.__parent.update()

    # 更新动画信息
    def updateAni(self,new_datas:dict):
        self.allAniDatas().update(new_datas)
        self.aniInit()
        self.createAni()

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

    def setStartValue(self, value) -> None:
        '''
            当这个值是 this 的时候,指向自己已经编写的属性值,
            如果没有这个属性值,将报错,
            如果这个属性中包含 color 则判定为颜色属性,否则判断为数值形
            如果这个属性值中包含px,pt 这里的,直接返回数值形
        :param value:
        :return:
        '''
        if self.isThis():
            attr = self.attr.lower()
            if self.qss.selector(self.selector).isAttr(attr):
                attrValue = self.qss.selector(self.selector).attr(self.attr) # Gets the value of the property
                if "color" in attr:
                    color = attrValue
                    if "rgb" in color.lower() or "rgba" in color.lower():
                        color_list=[int(i) for i in re.findall(r"[0-9]{1,3}",color)]
                        value = QColor(*color_list)
                    else:
                        value = QColor(color)
                elif "px" in attrValue or "pt" in attrValue:
                    value = int(re.findall(r"[0-9]+",attrValue)[0])
            else:
                raise Exception("The sv attribute is this, but QSS does not have this attribute!,{}".format(self.attr))

        super().setStartValue(value)

    def updateState(self, newState, oldState) -> None:
        super().updateState(newState,oldState)

    def interpolated(self, from_, to, progress: float):
        return super().interpolated(from_,to,progress)

    def __toValue(self,value):
        if isinstance(value, int):
            value = "{}{}".format(value,self.qssSuffix)
        elif isinstance(value, QColor):
            value = "rgba({},{},{},{})".format(*value.getRgb())

        else:
            raise Exception("This type is not supported yet.{}".format(value))
        return value

    def updateCurrentValue(self, value) -> None:
        self.qss.appendQSS(self.targetObj.styleSheet())
        self.qss.selector(self.selector).updateAttr(self.propertyName.decode(), self.__toValue(value))

# --------------


# 通用普通控件动画
class AnimationControl(PropertyAnimation):
    def __init__(self,parent:QObject,ani_data:dict,ani_obj_mode="control"):
        super().__init__(parent,ani_data,ani_obj_mode)

        self.setPropertyName(self.propertyName)
        self.createAni()

    def setStartValue(self, value) -> None:
        if self.isThis():
            if self.propertyName == b"geometry":
                value = self.targetObject().rect()
            elif self.propertyName == b"size":
                value = self.targetObject().size()
            elif self.propertyName == b"pos":
                value = self.targetObject().pos()
            elif self.propertyName == b"windowOpacity":
                value = self.targetObject().windowOpacity()
        super().setStartValue(value)


# 普通控件的特殊效果动画 - 阴影动画
class ShadowAnimation(PropertyAnimation):
    def __init__(self,parent:QObject,ani_data:dict,ani_obj_mode="control"):
        super().__init__(parent,ani_data,ani_obj_mode)

        if self.isEffect() is False:
            raise Exception("Special animation is not enabled,isEffect is False!")
        if self.targetObj.graphicsEffect() is None:
            self.__shadow = QGraphicsDropShadowEffect()
            self.targetObj.setGraphicsEffect(self.__shadow)
            self.__shadow.setOffset(0, 0)
        else:
            self.__shadow = self.targetObj.graphicsEffect()
        self.setPropertyName(self.propertyName)
        self.createAni()

    def setStartValue(self, value) -> None:
        value = value.value()
        if isinstance(value,int):
            self.__shadow.setBlurRadius(value)
            super().setStartValue(value)
        elif isinstance(value,QColor):
            self.__shadow.setColor(value)
            super().setStartValue(value)

    def updateCurrentValue(self, value: typing.Any) -> None:
        # print(value)
        if isinstance(value,int):
            print(value)
            self.__shadow.setBlurRadius(value)
        if isinstance(value,QColor):
            self.__shadow.setColor(value)



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
            super().setStartValue(value.value())

    def updateState(self, newState, oldState) -> None:
        super().updateState(newState, oldState)

    def updateCurrentValue(self, value) -> None:
        if self.drawSv():
            self.drawSv().setNumber(value)
            self.updateDraw()


# 返回动画类型
CreateAni = [AnimationControl,QSSPropertyAnimation,AnimationDrawValue]


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
    def createAni(self) -> CreateAni:
        if self.aniObjMode() == AnimationFactory.Control:
            if self.propertyName() in [b"geometry",b"size",b"pos",b"windowOpacity"]:
                ani = AnimationControl(*self.argc())
            elif self.propertyName() == b"shadow":
                ani = ShadowAnimation(*self.argc())
            elif self.propertyName() and self.aniData().get("selector",None):  # 处理所有qss属性
                ani = QSSPropertyAnimation(*self.argc())
            else:
                raise Exception("There is no animation property,{}!".format(self.propertyName()))
        elif self.aniObjMode() == AnimationFactory.Draw:
            if self.propertyName() == b"value":
                ani = AnimationDrawValue(*self.argc())
            else:
                raise Exception("There is no animation property!")
        else:
            raise Exception("This animation mode is not available!")

        return ani