from PyQtGuiLib.header import (
    QPropertyAnimation,
    QParallelAnimationGroup,
    QSequentialAnimationGroup,
    QPushButton,
    QObject,
    qt,
    Signal,
    QRect,
    QPoint
)

'''
    重构动画框架
    Animation 仅创建,管理,播放动画
'''

from PyQtGuiLib.animation.animationFactory import AnimationFactory

AniMode = int
ObjMode = str


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

        # 默认动画模式(并行)
        self.__ani_mode = AnimationAttr.Parallel
        # 默认动画时长
        self.__ani_duration = 1000
        # 默认动效
        self.__ani_special = AnimationAttr.InCurve
        # 默认动画循环次数
        self.__ani_loopCount = 1

        if parent:
            self.setParent(parent)

    def setParent(self,parent):
        self.__parent = parent

    def setAniMode(self,mode:AniMode):
        self.__ani_mode = mode

    def setDuration(self,duration:int):
        self.__ani_duration = duration

    def setSpecial(self,special):
        self.__ani_special = special

    def setLoopCount(self,count:int):
        self.__ani_loopCount = count

    def parent(self) -> QObject:
        return self.__parent

    def aniMode(self) -> AniMode:
        return self.__ani_mode

    def duration(self)->int:
        return self.__ani_duration

    def special(self):
        return self.__ani_special

    def loopCount(self)->int:
        return self.__ani_loopCount

    def aniObjMode(self) -> ObjMode:
        return self.__ani_obj_mode

    def isControlMode(self)->bool:
        return True if self.aniObjMode() == AnimationAttr.Control else False

    def isDrawMode(self)->bool:
        return True if self.aniObjMode() == AnimationAttr.Draw else False



class Animation(AnimationAttr):
    def __init__(self, parent: QObject = None, ani_obj_mode="control"):
        super(Animation, self).__init__(parent,ani_obj_mode)

        # 动画列表(里面每一个元素都是一个完整的动画对象)
        self.ani_list = []

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
        if not ani_data:
            return

        targetObject = ani_data.get("targetObj", None)

        duration = ani_data.get("duration", None)
        special = ani_data.get("special", None)
        loopCount = ani_data.get("loop", None)

        if duration is None:
            ani_data["duration"] = self.duration()
        if special is None:
            ani_data["special"] = self.special()
        if loopCount is None:
            ani_data["loopCount"] = self.loopCount()

        if self.isControlMode() and self.parent():
            ani = AnimationFactory(self.parent(),ani_data,self.aniObjMode()).createAni()
        elif self.isDrawMode():
            pass
        else:
            raise Exception("Pattern error,Only Animation.Control or Animation.Draw is supported!")

        self.ani_list.append(ani)


    def start(self):
        if self.aniMode() == Animation.Parallel:
            self.ani_group_obj = QParallelAnimationGroup(self.parent())
        if self.aniMode() == Animation.Sequential:
            self.ani_group_obj = QSequentialAnimationGroup(self.parent())

        for ani in self.ani_list:
            self.ani_group_obj.addAnimation(ani)

        self.ani_group_obj.start()

from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QPoint,
    qt,
    QPushButton,
)

class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

        self.btn = QPushButton("测试",self)
        self.btn.setStyleSheet('''
QPushButton{
background-color: red;
font-size:18px;
}
        ''')
        self.btn.move(50,50)
        self.btn.resize(130,60)

        self.ani = Animation(self)
        self.ani.setDuration(3000)

        self.ani.addAni({
            "targetObj":self.btn,
            "propertyName":b"geometry",
            "sv":self.btn.rect(),
            # "duration":1000,
            "ev":QRect(300,150,150,150),
            # "call":self.test,
            # "argc":(234,"hello")
        })

        self.ani.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())