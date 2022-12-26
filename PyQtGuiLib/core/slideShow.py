# -*- coding:utf-8 -*-
# @time:2022/12/2317:54
# @author:LX
# @file:SlideShow.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QResizeEvent,
    QPushButton,
    QPoint,
    QSize,
    QPropertyAnimation,
    Signal
)



'''

    轮播图功能
        风格: 扁平
'''
class SlideShow(QWidget):
    # 切换窗口事件
    switchWidgeted = Signal(int)

    # 扁平 风格
    FlatMode = "flat"  # 经典
    # 方向
    Left = "left"
    Right = "right"

    # 动画
    Translation = "translation"  # 平移

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(700, 300)

        self.show_mode = SlideShow.FlatMode # 展示模式
        self.animation_mode = SlideShow.Translation  # 动画模式

        self.animation_time = 300 # 毫秒

        self.index = [-1,0]  # 索引
        self.cu_index = self.index[1]  # 当前索引

        # 设置自动轮播,方向
        self.is_auto_slide = False
        self.direction = SlideShow.Right

        # 左右按钮
        self.left_btn = QPushButton("左",self)
        self.right_btn = QPushButton("右",self)
        self.left_btn.setObjectName("left_btn")
        self.right_btn.setObjectName("right_btn")
        self.left_btn.resize(50,50)
        self.right_btn.resize(50,50)
        self.left_btn.clicked.connect(lambda :self.roll_event(SlideShow.Left))
        self.right_btn.clicked.connect(lambda :self.roll_event(SlideShow.Right))
        self.btnStyle()

        # 窗口
        self.widgets = []  # 所有已经添加的窗口
        self.current_widgets = None # 当前已经展示出来的轮播窗口对象

        self.defaultBackground()

    def defaultBackground(self):
        '''
            默认背景,只有当前没有添加任何窗口时显示
        :return:
        '''
        print(self.isEmpty())
        if self.isEmpty():
            self.setStyleSheet('''
background-color:gray;
border-radius:5px;
            ''')

    # 自动轮播
    def setAutoSlideShow(self,b:bool,interval:int=2000,direction: str="right",is_not_show_btn:bool=True):
        '''
            b: 是否启动自动轮播
            interval:切换窗口的事件间隔
            direction:轮播方向
            is_not_show_btn:是否需要显示左右按钮
        '''
        self.is_auto_slide = b
        if b:
            self.startTimer(interval)

        self.setHideButtons(is_not_show_btn)

        self.direction = direction
        self.left_btn.setEnabled(not b)
        self.right_btn.setEnabled(not b)

    # 设置隐藏/显示左右按钮
    def setHideButtons(self,b:bool=False):
        if b:
            self.left_btn.hide()
            self.right_btn.hide()
        else:
            self.left_btn.show()
            self.right_btn.show()

    # 获取当前窗口的数量
    def getWidgetCount(self) -> int:
        return len(self.widgets)

    # 轮播事件
    def roll_event(self, direction: str):
        if self.show_mode == SlideShow.FlatMode:  # 经典模式
            widgets_count = self.getWidgetCount()

            if self.isEmpty():
                return

            self.index[0] += 1
            self.index[1] += 1

            if self.index[0] > widgets_count - 1:
                self.index[0] = 0

            if self.index[1] > widgets_count - 1:
                self.index[1] = 0

            self.cu_index = self.index[1] # 设置当前索引
            self.switchWidgeted.emit(self.index[1]) # 发送事件
            self.rollShow(direction)

    # 通过索引获取窗口
    def getWidget(self,index:int) -> QWidget:
        return self.widgets[index]

    def isEmpty(self) -> bool:
        return True if not self.widgets else False

    # 滚动显示
    def rollShow(self,direction: str):
        widget = self.widgets[self.index[0]] # type:QWidget
        widget2 = self.widgets[self.index[1]] # type:QWidget
        self.__createWidget(widget2)
        self.animation_(direction,widget,widget2)

    # 添加窗口
    def addWidget(self,widget:QWidget):
        self.widgets.append(widget)
        # 展示
        self.show_()

    # 移除窗口(2022.12.26该方法处于测试中,可能有BUG)
    def removeWidget(self,obj_or_index):
        '''
            obj_or_index: 窗口对象,或者是索引
        '''

        if isinstance(obj_or_index,int):
            widget = self.widgets[obj_or_index] # type:QWidget
            self.widgets.remove(widget)
            widget.hide()
        else:
            obj_or_index.hide()
            self.widgets.remove(obj_or_index)


    # 切换到指定窗口(暂时放弃改函数)
    # def setCurrentIndex(self,index:int=0,is_animation:bool=False):
    #     pass
        # if not is_animation:
        #     widget = self.getWidget(index)
        #
        #     self.__createWidget(widget)

    # 获取当前索引
    def getIndex(self)->int:
        if self.isEmpty():
           return None

        return self.cu_index

    # 切换到下一个窗口
    def next(self):
        self.roll_event(SlideShow.Right)

    # 切换到上一个窗口
    def up(self):
        self.roll_event(SlideShow.Left)

    # 两侧的按钮
    def btnPos(self):
        self.left_btn.move(5, self.height() // 2 - self.left_btn.height() // 2)
        self.right_btn.move(self.width() - self.right_btn.width() - 5,
                            self.height() // 2 - self.left_btn.height() // 2)

    # 按钮样式
    def btnStyle(self):
        self.left_btn.setStyleSheet('''
#left_btn{
background-color:transparent;
border:2px solid #73ffcc;
color:#73ffcc;
border-radius:5px;
}
#left_btn:hover{
border:2px solid #00557f;
}
        ''')
        self.right_btn.setStyleSheet('''
#right_btn{
background-color:transparent;
border:2px solid #73ffcc;
color:#73ffcc;
border-radius:5px;
}
#right_btn:hover{
border:2px solid #00557f;
}
                ''')

    # 返回左右按钮对象
    def getButtons(self) -> tuple:
        return self.left_btn,self.right_btn

    # 展示
    def show_(self):
        if self.show_mode == SlideShow.FlatMode:  # 经典模式

            if self.isEmpty():
                return

            # 优先展示第一个窗口
            widget = self.widgets[self.cu_index]  # type:QWidget
            self.__createWidget(widget)

            # 隐藏除了显示的以外的所有窗口
            for i in range(self.getWidgetCount()):
                if i != self.getIndex():
                    self.getWidget(i).hide()

    # 创建窗口
    def __createWidget(self,widget:QWidget):
        widget.setParent(self)
        widget.resize(QSize(self.width(),self.height()))
        widget.lower()
        widget.move(QPoint(0,0))
        widget.show()

    # 动画
    def animation_(self,direction:str,widget:QWidget,widget2:QWidget):
        if self.animation_mode == SlideShow.Translation:
            if len(self.widgets) >= 2:
                move_ani = QPropertyAnimation(self)
                move_ani2 = QPropertyAnimation(self)
                move_ani.setPropertyName(b"pos")
                move_ani2.setPropertyName(b"pos")
                move_ani.setTargetObject(widget)
                move_ani2.setTargetObject(widget2)

                move_ani.setStartValue(widget.pos())
                if direction == SlideShow.Right:
                    end_value,start_value = QPoint(widget.width(), 0),QPoint(-widget.width(), 0)
                elif direction == SlideShow.Left:
                    end_value,start_value = QPoint(-widget.width(), 0),QPoint(widget.width(), 0)
                move_ani.setEndValue(end_value)
                move_ani2.setStartValue(start_value)
                move_ani2.setEndValue(QPoint(0, 0))

                move_ani.setDuration(self.animation_time)
                move_ani2.setDuration(self.animation_time)

                move_ani.start()
                move_ani2.start()

    def resizeEvent(self, e:QResizeEvent) -> None:
        self.btnPos()
        self.show_()
        super().resizeEvent(e)

    def timerEvent(self, e) -> None:
        if self.is_auto_slide:
            self.roll_event(self.direction)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = SlideShow()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())