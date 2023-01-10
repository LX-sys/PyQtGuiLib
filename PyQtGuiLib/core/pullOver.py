from PyQtGuiLib.header import (
    QWidget,
    QThread,
    Signal,
    QPoint,
    QPropertyAnimation,
    desktopCenter,
    desktopSize,
    qt
)


class MonitoThread(QThread):
    winPosed = Signal(QPoint)  # 窗口位置线程

    def __init__(self,widget:QWidget,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.widget = widget
        self.stop = False # 暂停
        self.termination_th = False # 终止
        self.monito_ms = 150  # 检测已毫秒为单位

    def setTermination(self,b:bool):
        self.termination_th = b

    def setStop(self,b:bool):
        self.stop = b

    def run(self) -> None:
        while True:
            if self.stop:
                self.msleep(self.monito_ms<<2)
                continue

            if self.termination_th:
                break
            self.winPosed.emit(self.widget.pos())
            self.msleep(self.monito_ms)


# 窗口靠边
class PullOver:

    # 弹力
    OutBounce = qt.OutBounce


    def __init__(self,parent:QWidget,*args,**kwargs):
        self.parent = parent
        super().__init__(*args,**kwargs)

        self.scope = 10

        self.move_ani = QPropertyAnimation(self.parent)
        self.move_ani.setPropertyName(b"pos")
        self.move_ani.setTargetObject(self.parent)
        self.monitoth = MonitoThread(self.parent)
        self.monitoth.start()

    # 设置动效
    def setEasingCurve(self,easing):
        if easing:
            self.move_ani.setEasingCurve(easing)

    # 核心方法
    def pullover(self,btn_obj:QWidget,pos:QPoint=None,small_btn_pos:QPoint=None):
        '''
            btn_obj:是一个具有clicked点击事件的按钮,或者其他控件
            pos:窗口显示的位置,默认居中
            small_btn_pos:窗口隐藏后按钮显示的位置
        '''
        if pos is None:
            pos = self.center()

        self.showWin(btn_obj,pos)
        self.hideWin(btn_obj,small_btn_pos)

    def showWin(self,btn_obj:QWidget,pos:QPoint):
        btn_obj.clicked.connect(lambda: self.show_win_event(btn_obj, pos))

    def hideWin(self,btn_obj:QWidget,small_win_pos:QPoint=None):
        self.monitoth.winPosed.connect(lambda pos: self.winHide_event(btn_obj, pos,small_win_pos))

    # 靠边隐藏
    def winHide_event(self,btn_obj:QWidget,pos:QPoint,small_btn_pos:QPoint=None):
        x,y = pos.x(),pos.y()
        # s_count = QApplication.desktop().screenCount()
        desktop_w = desktopSize().width()
        desktop_h = desktopSize().height()
        def _t(parent, self):
            parent.hide()
            btn_obj.move(small_btn_pos)
            btn_obj.show()
            self.move_ani.finished.disconnect()

        # Window current position
        pos_ = self.parent.pos()
        px, py = pos.x(), pos_.y()

        if x <= self.scope:
            if small_btn_pos is None:
                small_btn_pos = QPoint(0, desktop_h>>1)
                # small_btn_pos = QPoint(0, py)

            self.monitoth.setStop(True)
            self.move_ani.setStartValue(pos_)
            self.move_ani.setEndValue(QPoint(-self.parent.width(),py))
            self.move_ani.start()
            # 解开暂停
            self.move_ani.finished.connect(lambda :_t(self.parent,self))
        elif desktop_w - (x + self.parent.width()) <= self.scope:  # right
            if small_btn_pos is None:
                small_btn_pos = QPoint(desktop_w - btn_obj.width(), desktop_h>>1)

            self.monitoth.setStop(True)
            self.move_ani.setStartValue(self.parent.pos())
            self.move_ani.setEndValue(QPoint(desktop_w+self.parent.width(), py))
            self.move_ani.start()
            # 解开暂停
            self.move_ani.finished.connect(lambda: _t(self.parent, self))
        elif y <= self.scope:
            if small_btn_pos is None:
                small_btn_pos = QPoint(desktop_w>>1,0)

            self.monitoth.setStop(True)
            self.move_ani.setStartValue(self.parent.pos())
            self.move_ani.setEndValue(QPoint(px,-self.parent.height()))
            self.move_ani.start()
            # 解开暂停
            self.move_ani.finished.connect(lambda :_t(self.parent,self))

    def show_win_event(self,btn_obj:QWidget,pos:QPoint):
        btn_obj.hide()
        self.parent.show()
        self.move_ani.setStartValue(self.parent.pos())
        self.move_ani.setEndValue(pos)
        self.move_ani.start()
        def _t(self):
            self.monitoth.setStop(False)
            self.move_ani.finished.disconnect()
        self.move_ani.finished.connect(lambda :_t(self))

    def center(self):
        f = self.parent.frameGeometry()
        f.moveCenter(desktopCenter())
        return f.topLeft()

    '''
        请在你的窗口中,重写关闭事件,并加入这一句话
    '''
    def closeThread(self):
        # 在关闭之前,先终止线程
        self.monitoth.setTermination(True)
