

from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QWidget,
    QThread,
    QCloseEvent,
    Signal,
    QPoint,
    QPropertyAnimation,
    QEasingCurve,
    QDesktopWidget,
)

from PyQtGuiLib.core.widgets import ButtonWidget


class MonitoThread(QThread):
    winPosed = Signal(QPoint)  # 窗口位置线程

    def __init__(self,widget:QWidget,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.widget = widget
        self.stop = False # 暂停
        self.termination_th = False # 终止
        self.monito_ms = 20  # 检测已毫秒为单位

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


class PullOverWidget(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(500,500)

        self.show_btn = ButtonWidget()
        self.show_btn.resize(70, 70)
        self.show_btn.setObjectName("show_btn")
        self.show_btn.setStyleSheet('''
        #show_btn{
        background-color:green;
        border-radius:35px;
        }
        ''')
        self.show_btn.clicked.connect(self.show_win_event)
        # 动画
        self.move_ani = QPropertyAnimation(self)
        self.move_ani.setPropertyName(b"pos")
        self.move_ani.setTargetObject(self)
        self.move_ani.setEasingCurve(QEasingCurve.OutBounce)

        self.monitoth = MonitoThread(self)
        self.monitoth.start()
        self.monitoth.winPosed.connect(self.winHide_event)

    # 靠边隐藏
    def winHide_event(self,pos:QPoint):
        x,y = pos.x(),pos.y()
        if x <= 10:
            self.monitoth.setStop(True)
            self.move_ani.setStartValue(self.pos())
            self.move_ani.setEndValue(QPoint(-self.width(),300))
            self.move_ani.start()
            def _(self):
                self.hide()
                self.show_btn.move(0,300)
                self.show_btn.show()
                self.move_ani.disconnect()
            # 解开暂停
            self.move_ani.finished.connect(lambda :_(self))

    def show_win_event(self):
        self.show_btn.hide()
        self.show()
        self.move_ani.setStartValue(self.pos())
        self.move_ani.setEndValue(self.center())
        self.move_ani.start()
        def _(self):
            self.monitoth.setStop(False)
            self.move_ani.disconnect()
        self.move_ani.finished.connect(lambda :_(self))

    def center(self):
        f = self.frameGeometry()
        c = QDesktopWidget().availableGeometry().center()
        f.moveCenter(c)
        return f.topLeft()

    def closeEvent(self, event:QCloseEvent) -> None:
        # 在关闭之前,先终止线程
        self.monitoth.setTermination(True)
        super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = PullOverWidget()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
