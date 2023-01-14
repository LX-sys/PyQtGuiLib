from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QWidget,
    QHBoxLayout,
    QPushButton,
    QSize,
    QPaintEvent,
    QPainter,
    QPropertyAnimation,
    QPoint,
    Signal,
    qt
)

'''
    滚动栏
'''


# 堆栈(管理隐藏的控件)
class Stack:
    def __init__(self):
        self.hide_controls = []

    def push(self,e):
        self.hide_controls.append(e)

    def pop(self):
        if self.isEmpty():
            return None
        return self.hide_controls.pop(-1)

    def isEmpty(self) -> bool:
        if not self.hide_controls:
            return True
        return False

    def show(self):
        print(self.hide_controls)


# 控件管理
class ControlsSystem:
    def __init__(self):
        self.controls = []
        self.stack = Stack()

    def append(self,e):
        self.controls.append(e)

    # 隐藏头部元素
    def hideHead(self):
        e = self.controls.pop(0)
        self.stack.push(e)
        return e

    # 显示头部元素
    def showHead(self):
        e = self.stack.pop()
        if e:
            self.controls.insert(0,e)
            return e

    def all(self)->list:
        return self.controls

    def isEmpty(self)->bool:
        if len(self.controls) == 1:
            return True
        return False

    def isHideEmpty(self)->bool:
        if len(self.stack.hide_controls) == len(self.controls)-1:
            return True
        return False

    def show(self):
        print(self.controls)
        self.stack.show()

# ss = ControlsSystem()
# for i in range(1,7):
#     ss.append(i)
#
# for _ in range(3):
#     ss.hideHead()
#
# for _ in range(2):
#     ss.showHead()
# ss.show()


class RollWidget(QWidget):
    # 滚动栏 改变信号
    changed = Signal(QWidget)

    # 动画效果
    InCurve = qt.InCurve
    OutBounce = qt.OutBounce
    CosineCurve = qt.CosineCurve
    SineCurve = qt.SineCurve

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.resize(800,60)

        # 样式表生效
        self.setAttribute(qt.WA_StyledBackground, True)

        # 控件管理系统对象
        self.controls = ControlsSystem()

        self.is_press = True # 按下标记,在按下时,让自动布局失效

        # 左边距
        self.left_margin = 10

        # 控件的起始位置,最左边的边距
        self.x = 3
        self.padding = 9

        # 控件默认大小
        self.default_size = QSize(70,50)
        self.btn_size = QSize(30,30) # 按钮默认大小

        # 动画是否启用,持续时间,动画特效
        self.ani_enabled = True
        self.ani_duration = 200
        self.ani_special = RollWidget.InCurve

        self.Init()
        self.myEvent()
        self.defaultStyle()

    # 初始化
    def Init(self):
        # 左右布局
        self.hlay = QHBoxLayout(self)
        self.hlay.setContentsMargins(0,0,0,0)
        self.hlay.setSpacing(0)

        # 左右布局 - 窗口
        self.left_widget = QWidget()
        self.right_widget = QWidget()
        self.right_widget.setFixedWidth(100)
        self.left_widget.setObjectName("left_widget")
        self.right_widget.setObjectName("right_widget")

        # 右布局内部布局
        self.hhlay = QHBoxLayout(self.right_widget)
        self.left_btn = QPushButton("<")
        self.right_btn = QPushButton(">")
        self.left_btn.setObjectName("left_btn")
        self.right_btn.setObjectName("right_btn")
        self.left_btn.setFixedSize(self.btn_size)
        self.right_btn.setFixedSize(self.btn_size)

        self.hlay.addWidget(self.left_widget)
        self.hlay.addWidget(self.right_widget)
        self.hhlay.addWidget(self.left_btn)
        self.hhlay.addWidget(self.right_btn)

    # 默认样式
    def defaultStyle(self):
        self.setStyleSheet('''
#left_widget{
background-color:rgb(208, 208, 208);
}
#right_widget{
background-color: rgb(63, 63, 63);
}
#left_btn{
background-color:transparent;
border:2px solid #73ffcc;
color:#73ffcc;
border-radius:5px;
}
#left_btn:hover{
border:2px solid rgb(204, 204, 204);
}
#right_btn{
background-color:transparent;
border:2px solid #73ffcc;
color:#73ffcc;
border-radius:5px;
}
#right_btn:hover{
border:2px solid rgb(204, 204, 204);
}
                ''')

    # 设置动画是否启用
    def setAniEnabled(self,b:bool):
        self.ani_enabled = b

    # 设置持续时间
    def setAniDuration(self, duration:int):
        self.ani_duration = duration

    # 设置动画特效
    def setAniSpecial(self,special):
        self.ani_special = special

    # 自动布局
    def updateLayout(self):
        # 刷新起始位置
        self.x = 3
        center_h = self.height()//2
        for w in self.controls.all():  # type:QWidget
            w.move(self.x+self.left_margin,center_h-w.height()//2)
            self.x += w.width()+self.padding
            w.show()

    # 添加控件
    def addWidget(self,widget:QWidget):
        # 公共设置
        widget.setParent(self.left_widget)
        widget.setFixedSize(self.default_size)

        self.controls.append(widget)

    # 移除控件(未写)
    def removeWidget(self,widget:QWidget):
        pass

    # 移动事件
    def move_event(self,direction=""):
        self.is_press = False  # 关闭自动布局
        if direction == "left" and not self.controls.isEmpty():
            widget = self.controls.hideHead()
            self.changed.emit(widget)  # 发送信号
            widget.hide()
        elif direction == "right" and not self.controls.stack.isEmpty():
            widget = self.controls.showHead()
            self.changed.emit(widget) # 发送信号
            widget.show()
        # self.controls.show()
        if self.ani_enabled:
            self.ani_(direction)
        else:
            self.is_press = True

    # 动画
    def ani_(self,direction=""):
        def _t(self):
            self.updateLayout()
            self.is_press = True # 重启自动布局

        center_h = self.height() // 2
        for i, wid in enumerate(self.controls.all()):
            ani = QPropertyAnimation(self.left_widget)
            ani.setPropertyName(b"pos")
            ani.setDuration(self.ani_duration)
            ani.setTargetObject(wid)
            ani.setEasingCurve(self.ani_special)
            s_pos = wid.pos()  # type:QPoint
            if direction == "left":
                x = s_pos.x() - wid.width()- self.left_margin
            elif direction == "right":
                x = s_pos.x() + wid.width()+ self.left_margin
            ani.setStartValue(s_pos)
            ani.setEndValue(QPoint(x,center_h - wid.height() // 2))
            ani.finished.connect(lambda: _t(self))  # 刷新右移动动画
            ani.start()

    # 事件
    def myEvent(self):
        self.left_btn.clicked.connect(lambda :self.move_event("left"))
        self.right_btn.clicked.connect(lambda :self.move_event("right"))

    # 返回按钮
    def buttons(self)->tuple:
        return self.left_btm,self.right_btn

    def paintEvent(self, e:QPaintEvent) -> None:
        painter = QPainter(self)

        if self.is_press:
            self.updateLayout()

        painter.end()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = RollWidget()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())