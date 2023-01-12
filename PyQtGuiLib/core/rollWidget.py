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
    QPropertyAnimation
)

'''
    滚动栏
'''

# 堆栈
class Stack:
    def __init__(self):
        self.hide_controls = []

    def push(self,e):
        self.hide_controls.append(e)

    def pop(self):
        return self.hide_controls.pop(-1)

    def isEmpty(self) -> bool:
        if not self.hide_controls:
            return True
        return False

    # 隐藏当对象
    def cu_hide_obj(self):
        if self.isEmpty():
            return None
        return self.hide_controls[-1]

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
        self.stack.push(self.controls.pop(0))

    # 显示头部元素
    def showHead(self):
        self.controls.insert(0,self.stack.pop())

    # 隐藏当对象
    def cuObj(self)->QWidget:
        return self.stack.cu_hide_obj()

    def all(self)->list:
        return self.controls

    def isEmpty(self)->bool:
        if not self.controls:
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
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.resize(800,60)

        self.setStyleSheet('''
#left_widget{
background-color:red;
}
#right_widget{
background-color:blue;
}
        ''')

        # 控件表,隐藏的控件列表(栈)
        self.controls = ControlsSystem()

        self.hlay = QHBoxLayout(self)
        self.hlay.setContentsMargins(0,0,0,0)
        self.hlay.setSpacing(0)

        # 左右布局
        self.left_widget = QWidget()
        self.right_widget = QWidget()
        self.right_widget.setFixedWidth(100)
        self.left_widget.setObjectName("left_widget")
        self.right_widget.setObjectName("right_widget")

        # 右布局内部布局
        self.hhlay = QHBoxLayout(self.right_widget)
        self.left_btn = QPushButton("<")
        self.right_btn = QPushButton(">")

        # 左边距
        self.left_margin = 10

        # 控件的起始位置,最左边的边距
        self.x = 3
        self.padding = 9

        # 控件默认大小
        self.default_size = QSize(70,50)

        for i in range(6):
            btn = QPushButton("test_{}".format(i))
            btn.setStyleSheet("background-color:green;")
            self.addWidget(btn)

        self.Init()
        self.myEvent()

    def Init(self):
        self.hlay.addWidget(self.left_widget)
        self.hlay.addWidget(self.right_widget)
        self.hhlay.addWidget(self.left_btn)
        self.hhlay.addWidget(self.right_btn)
        # self.update()

    # 自动布局
    def updateLayout(self):
        # 刷新起始位置
        self.x = 3

        center_h = self.height()//2
        for w in self.controls.all():  # type:QWidget
            w.move(self.x+self.left_margin,center_h-w.height()//2)
            self.x+= w.width()+self.padding
            # w.show()


    # 添加控件
    def addWidget(self,widget:QWidget):
        # 公共设置
        widget.setParent(self.left_widget)
        widget.setFixedSize(self.default_size)

        self.controls.append(widget)

    # 左移动事件
    def move_event(self,direction=""):
        # if self.controls.isEmpty():
        #     self.update()
        #     return
        #
        # ani = QPropertyAnimation(self.title)
        # ani.setTargetObject(self.title)
        # ani.setPropertyName(b"pos")
        # ani.setDuration(300)

        if direction == "left":
            self.controls.hideHead()
            widget = self.controls.cuObj()
            print(widget.text())
        elif direction == "right":
            self.controls.showHead()
            widget = self.controls.cuObj()
            print(widget.text())
        self.update()

    def myEvent(self):
        self.left_btn.clicked.connect(lambda :self.move_event("left"))
        self.right_btn.clicked.connect(lambda :self.move_event("right"))

    def paintEvent(self, e:QPaintEvent) -> None:
        painter = QPainter(self)

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