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

    def setAniGroupObj(self,obj:QParallelAnimationGroup):
        if isinstance(obj,QParallelAnimationGroup) or isinstance(obj,QSequentialAnimationGroup):
            self.__ani_group_obj = obj
        else:
            raise Exception("Attribute error!")

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

    def aniGroupObj(self)->QParallelAnimationGroup:
        return self.__ani_group_obj

    def isAniGroupObj(self)->bool:
        return True if self.aniGroupObj() else False

    def isControlMode(self)->bool:
        return True if self.aniObjMode() == AnimationAttr.Control else False

    def isDrawMode(self)->bool:
        return True if self.aniObjMode() == AnimationAttr.Draw else False


# 动画类
class Animation(AnimationAttr):
    def __init__(self, parent: QObject = None, ani_obj_mode="control"):
        super(Animation, self).__init__(parent,ani_obj_mode)

        # 动画列表(里面每一个元素都是一个完整的动画对象)
        self.ani_list = []

    # 设置通用属性
    def __setGeneralAttr(self,ani_data):
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

        self.__setGeneralAttr(ani_data)

        if self.isControlMode() and self.parent():
            ani = AnimationFactory(self.parent(),ani_data,self.aniObjMode()).createAni()
        elif self.isDrawMode():
            ani_data["targetObj"] = QObject()
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
        if self.aniMode() != Animation.Sequential:
            raise Exception("Current animation mode is not Animation.Sequential")

        if not ani_data:
            return

        self.__setGeneralAttr(ani_data)

        if self.isControlMode() and self.parent():
            '''
                如果有回调函数,保存之后,先移除掉,最后添加在末尾
            '''
            Call = ani_data.get("call",None)
            CallAgrc = ani_data.get("argc",None)
            if Call:del ani_data["call"]
            if CallAgrc:del ani_data["argc"]

            # 首先创建出 初始动画
            ani = AnimationFactory(self.parent(),ani_data,self.aniObjMode()).createAni()
            self.ani_list.append(ani)
            sv = ani.endValue()
            # 在创建出后续的连续动画
            for ev in variation:
                if ev == variation[-1]: # 这里判断是否是最后一项数值
                    if Call:ani_data["call"] = Call
                    if CallAgrc:ani_data["argc"] = CallAgrc
                e_ani = AnimationFactory(self.parent(),ani_data,self.aniObjMode()).createAni()
                e_ani.setStartValue(sv)
                e_ani.setEndValue(ev)
                sv = ev
                self.ani_list.append(e_ani)
        elif self.isDrawMode():
            ani_data["targetObj"] = QObject()
        else:
            raise Exception("Pattern error,Only Animation.Control or Animation.Draw is supported!")

    def pause(self,call=None,argc=None):
        if self.isAniGroupObj():
            self.aniGroupObj().pause()

            if call:
                if argc:
                    call(*argc)
                else:
                    call()

    def resume(self,call=None,argc=None):
        if self.isAniGroupObj():
            self.aniGroupObj().resume()

            if call:
                if argc:
                    call(*argc)
                else:
                    call()

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

# 测试用例
# ----------------------------

from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QPoint,
    qt,
    QPushButton,
    QSize,
    QPainter,
    QColor
)

class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

        self.swBtn = QPushButton("开关",self)
        self.swBtn.move(150,50)

        self.btn = QPushButton("测试",self)
        self.btn.setStyleSheet('''
QPushButton{
background-color: red;
font-size:18px;
border-width:1px;
border-color:rgb(85, 255, 0);
border-style:solid;
}
        ''')
        self.btn.move(50,50)
        self.btn.resize(130,60)

        self.ani = Animation(self)
        self.ani.setDuration(3000)

        self.swBtn.clicked.connect(lambda :self.ani.aniSwitch(self.swBtn))

        # self.ani.addAni({
        #     "targetObj":self.btn,
        #     "propertyName":b"geometry",
        #     "sv":self.btn.rect(),
        #     "ev":QRect(300,150,150,150),
        #     "call":self.test
        # })
        # self.ani.addAni({
        #     "targetObj":self.btn,
        #     "propertyName":b"size",
        #     "sv":self.btn.size(),
        #     "ev":QSize(200,100),
        #     "call":self.test
        # })
        # self.ani.addAni({
        #     "targetObj":self.btn,
        #     "propertyName":b"pos",
        #     "sv":self.btn.pos(),
        #     "ev":QPoint(200,100),
        #     "call":self.test
        # })
        # self.ani.addAni({
        #     "targetObj": self.btn,
        #     "propertyName": b"backgroundColor",
        #     "sv": QColor(0,255,255),#
        #     "ev": QColor(255,0,0),#
        #     "call": self.test,
        #     "selector":"QPushButton"
        # })
        # self.ani.addAnis({
        #     "targetObj":self.btn,
        #     "propertyName":b"geometry",
        #     "sv":self.btn.rect(),
        #     "ev":QRect(300,150,150,150),
        #     "call":self.test
        # },{
        #     "targetObj": self.btn,
        #     "propertyName": b"backgroundColor",
        #     "sv": QColor(0,255,255),#
        #     "ev": QColor(255,0,0),#
        #     "call": self.test,
        #     "selector":"QPushButton"
        # })

        # 连续动画测试
        # self.ani.setAniMode(Animation.Sequential)
        # self.ani.addSeriesAni({
        #     "targetObj":self.btn,
        #     "propertyName":b"size",
        #     "sv":self.btn.size(),
        #     "ev":QSize(200,100),
        #     "call":self.test
        # },
        # [QSize(50,50),QSize(30,30),QSize(200,200)])
        self.ani.addAni({
            "targetObj": self.btn,
            "propertyName": b"borderColor",
            "sv": QColor(0,255,0),#
            "ev": QColor(20,88,152),#
            "call": self.test,
            "selector":"QPushButton"
        })
        self.ani.start()

        self.myrect = QRect(100,100,60,60)
        self.r = 0

    def test(self,obj):
        print("obj:",obj)

    def paintEvent(self, e) -> None:
        painter = QPainter(self)
        painter.setBrush(QColor(0,255,0))
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)
        # painter.rotate(self.rotate_a.valve())
        painter.drawRoundedRect(self.myrect,self.r,self.r)
        painter.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())