
from PyQtGuiLib.header import (
    QPropertyAnimation,
    QObject
)
from PyQtGuiLib.styles import QssStyleAnalysis
'''

    动画工厂
'''
class AnimationFactory:
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
        if self.propertyName() == b"geometry":
            ani = AnimationGeometry(self.parent(),self.aniData(),None,self.aniObjMode())
        else:
            raise Exception("This animation mode is not available!")
        return ani



class AnimationGeometry(QPropertyAnimation):
    Parallel = 1
    Sequential = 2
    # 动画对象模式
    Control = "control"  # 动画作用在普通控件上面
    Draw = "draw"  # 动画作用在绘制的图形上面

    def __init__(self,parent:QObject,ani_data:dict,qss:QssStyleAnalysis=None,ani_obj_mode="control"):
        self.__parent = parent
        super().__init__(parent)

        # 动画对象模式
        self.__ani_obj_mode = ani_obj_mode

        # 信息
        # self.__ani_all_info = ani_data

        self.setPropertyName(b"geometry")

        self.createAni(ani_data)

    def aniObjMode(self):
        return self.__ani_obj_mode

    def createAni(self,ani_data):
        targetObj = ani_data.get("targetObj", None)
        propertyName = ani_data.get("propertyName", None)
        sv = ani_data.get("sv", None)
        atv = ani_data.get("atv", None)
        ev = ani_data.get("ev", None)
        call = ani_data.get("call", None)
        call_argc = ani_data.get("argc", None)
        selector = ani_data.get("selector", None)
        duration = ani_data.get("duration", self.duration())
        # special = ani_data.get("special", self.special())
        loopCount = ani_data.get("loop", self.loopCount())

        self.setTargetObject(targetObj)
        self.setDuration(duration)
        # self.setSpecial(special)
        self.setLoopCount(loopCount)

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

        if call:
            if self.aniObjMode() == AnimationGeometry.Control:
                if call_argc:
                    self.finished.connect(lambda :call(targetObj,*call_argc))
                else:
                    self.finished.connect(lambda :call(targetObj))
            elif self.aniObjMode() == AnimationGeometry.Draw:
                if call_argc:
                    self.drawfinished.connect(lambda :call(targetObj,*call_argc))
                else:
                    self.drawfinished.connect(lambda :call(targetObj))