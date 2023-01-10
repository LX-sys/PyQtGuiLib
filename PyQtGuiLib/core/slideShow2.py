# -*- coding:utf-8 -*-
# @time:2023/1/10 12:41
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
    QLabel,
    qt,
    QPoint,
    QSize,
    QPropertyAnimation,
    Signal
)

from PyQtGuiLib.styles import ButtonStyle

'''

    轮播图功能
        风格: 扁平
'''

# 滚轮类
class Idler:
    def __init__(self):
        # self.lists = [1,2,3,4,5]
        self.lists = []
        # 双指针
        self.s_p = 0
        self.e_p = 1

        # 首次调用
        self.is_rigth = True
        self.is_left = True

        # 当前点击的方向
        self.cu_d = None

    # 添加窗口
    def addWidget(self,widget:QWidget):
        self.lists.append(widget)

    # 移除窗口
    def removeWidget(self,widget:QWidget):
        self.lists.remove(widget)

    # 长度
    def count(self)->int:
        return len(self.lists)

    # 返回当前两个指针,指向的窗口
    def getWidgtes(self)->tuple:
        if self.cu_d == "left":
            return (self.lists[self.e_p],self.lists[self.s_p])
        return (self.lists[self.s_p],self.lists[self.e_p])

    def widgets(self)->list:
        return self.lists

    # 滚轮向下走一步
    def next(self):
        self.cu_d = "right"
        # 如果首次点击的是下一步
        if self.is_rigth:
            self.s_p,self.e_p = self.count() - 1,0
            self.is_rigth,self.is_left = False,False

        self.s_p += 1
        self.e_p += 1
        if self.s_p > self.count()-1:
            self.s_p = 0
        if self.e_p > self.count()-1:
            self.e_p = 0

    # 滚轮向上走一步
    def up(self):
        self.cu_d = "left"
        self.s_p -= 1
        self.e_p -= 1
        if self.s_p < 0:
            self.s_p = self.count()-1
        if self.e_p < 0:
            self.e_p = self.count()-1



# dl = Idler()
# dl.next()
# print(dl.getWidgtes())
# dl.next()
# print(dl.getWidgtes())
# dl.next()
# print(dl.getWidgtes())
# dl.next()
# print(dl.getWidgtes())
# dl.next()
# print(dl.getWidgtes())
# print("===")
# dl.up()
# print(dl.getWidgtes())
# dl.up()
# print(dl.getWidgtes())



class SlideShow(QWidget):
    # 切换窗口事件
    switchWidgeted = Signal(int)

    # 扁平 风格
    FlatMode = "flat"  # 经典

    # 动画的方向模式
    Ani_Left = "left"
    Ani_Right = "right"
    Ani_Down = "down"
    Ani_Up = "up"

    # 动画
    Translation = "translation"  # 平移

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(700, 300)

        self.show_mode = SlideShow.FlatMode # 展示模式
        self.animation_mode = SlideShow.Translation  # 动画模式

        # 滚轮类
        self.idler = Idler()

        self.animation_time = 300 # 毫秒

        # 设置自动轮播,自动轮播的方向组
        self.is_auto_slide = False
        self.auto_direction =SlideShow.Ani_Right

        # 当前显示的窗口
        self.current_widget = None  # type:QWidget

        self.createBtn()

        for i in range(1,5):
            l = QLabel(str(i))
            l.setAlignment(qt.AlignCenter)
            l.setStyleSheet(ButtonStyle.contrastStyle())
            self.addWidget(l)

    # 创建按钮
    def createBtn(self):
        # 左右按钮
        self.Ani_Left_btn = QPushButton("左", self)
        self.Ani_Right_btn = QPushButton("右", self)
        self.Ani_Left_btn.setObjectName("Ani_Left_btn")
        self.Ani_Right_btn.setObjectName("Ani_Right_btn")
        self.Ani_Left_btn.resize(50, 50)
        self.Ani_Right_btn.resize(50, 50)
        self.btnStyle()
        self.Ani_Left_btn.clicked.connect(lambda :self.LR_event(SlideShow.Ani_Left))
        self.Ani_Right_btn.clicked.connect(lambda :self.LR_event(SlideShow.Ani_Right))

    # 按钮样式
    def btnStyle(self):
        self.Ani_Left_btn.setStyleSheet('''
#Ani_Left_btn{
background-color:transparent;
border:2px solid #73ffcc;
color:#73ffcc;
border-radius:5px;
}
#Ani_Left_btn:hover{
border:2px solid #00557f;
}
        ''')
        self.Ani_Right_btn.setStyleSheet('''
#Ani_Right_btn{
background-color:transparent;
border:2px solid #73ffcc;
color:#73ffcc;
border-radius:5px;
}
#Ani_Right_btn:hover{
border:2px solid #00557f;
}
                ''')

    # 两侧的按钮
    def btnPos(self):
        self.Ani_Left_btn.move(5, self.height() // 2 - self.Ani_Left_btn.height() // 2)
        self.Ani_Right_btn.move(self.width() - self.Ani_Right_btn.width() - 5,
                            self.height() // 2 - self.Ani_Left_btn.height() // 2)

    # 按钮事件
    def LR_event(self,d:str):
        self.idler.next()
        self.__animation()

    # 添加窗口
    def addWidget(self,widget:QWidget):
        widget.setParent(self)
        widget.lower()
        widget.resize(self.size())

        self.current_widget = widget
        self.hideItWidget()
        self.idler.addWidget(widget)

    # 隐藏其他窗口
    def hideItWidget(self):
        if not self.current_widget:
            return
        for w in self.idler.widgets():
            if self.current_widget != w and not w.isHidden():
                w.hide()

    # 移除窗口
    def removeWidget(self,widget:QWidget):
        self.idler.removeWidget(widget)

    # 切换到指定窗口(暂时放弃改函数)
    def setCurrentIndex(self,index:int=0,is_animation:bool=False):
        pass

    # 过渡动画
    def __animation(self):
        if self.auto_direction == SlideShow.Ani_Up:
            pass
        elif self.auto_direction == SlideShow.Ani_Down:
            pass
        elif self.auto_direction == SlideShow.Ani_Left:
            pass
        else: # 默认右
            l = self.idler.getWidgtes()[0]
            r = self.idler.getWidgtes()[1]
            print("当前:",l.text(),r.text())
            # self.auto_direction == SlideShow.Ani_Right:
            # pass


    def resizeEvent(self, event:QResizeEvent) -> None:
        self.btnPos()
        # 只渲染当前的页面
        if self.current_widget:
            self.current_widget.resize(event.size())

        super().resizeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = SlideShow()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())