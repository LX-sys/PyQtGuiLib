from PyQtGuiLib.header import (
    QWidget,
    Widget,
    QPainter,
    QBrush,
    QColor,
    QFont,
    QPaintEvent,
    qt,
    Qt,
    textSize,
    QThread,
    Signal,
    QGraphicsDropShadowEffect,
    QPropertyAnimation,
    QPoint,
    QObject
)

U_Center = "U_Center"
Left_Down = "Left_Down"
Rigth_Down = "Rigth_Down"

class Time(QThread):
    finish = Signal()
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self._time = 2500

    def setTime(self,d):
        self._time = d

    def run(self) -> None:
        self.msleep(self._time)
        self.finish.emit()


'''
    通知栏
'''
class Notice(Widget):
    finish = Signal(QObject)

    def __init__(self,parent=None):
        super().__init__(parent)
        self.resize(220,40)
        self.__parent = parent

        self.setWindowFlags(qt.FramelessWindowHint|qt.WindowStaysOnTopHint|qt.WindowTransparentForInput)
        self.setAttribute(qt.WA_TranslucentBackground,True)

        self.__text = "hello wrold"
        self.__pos = U_Center

        self.tth = Time()
        self.tth.finish.connect(self.finish_event)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(2)
        self.shadow.setOffset(2,2)
        self.shadow.setColor(qt.gray)
        self.setGraphicsEffect(self.shadow)

    def finish_event(self):
        self.finish.emit(self)
        self.deleteLater()
        self.__parent.update()

    def setText(self,text,interval=8000):
        self.__text = text
        self.updatePos()
        self.tth.setTime(interval)
        self.tth.start()

    def text(self)->str:
        return self.__text

    def updatePos(self):
        w = self.__parent.width()
        h = self.__parent.height()

        if self.__pos == Left_Down:
            self.move(self.get_margin(),h-self.height()-self.get_margin()*2)
        elif self.__pos == Rigth_Down:
            self.move(w-self.width()-self.get_margin(),h-self.height()-self.get_margin()*2)
        else:
            self.move(w//2-self.width()//2,self.get_margin())

    def paintEvent(self, event:QPaintEvent) -> None:
        painter = QPainter(self)

        painter.setPen(qt.NoPen)
        bru = QBrush(self.get_backgroundColor())
        painter.setBrush(bru)

        painter.drawRoundedRect(self.rect(),self.get_radius(),self.get_radius())

        painter.setPen(self.get_color())
        font = QFont(self.text())
        font.setPointSize(self.get_fontSize())

        painter.setFont(font)

        fs = textSize(font,self.text())
        x = self.width()//2 - fs.width()//2
        y = self.height()//2 + fs.height()//2
        painter.drawText(x,y,self.text())

        painter.end()

    def closeEvent(self, event) -> None:
        super().closeEvent(event)


class Notices(QObject):
    def __init__(self,parent:QWidget):
        super().__init__(parent)
        self.winp = parent

        # 通知组
        self.notices = []
        # 记录高度
        self.notice_heights = []

        self.spacing = 9

        self.style = ""

    def setSpacing(self,n):
        self.spacing = n

    def count(self)->int:
        return len(self.notices)

    def finish_event(self,obj:QObject):
        self.notices.remove(obj)
        # 未写完
        if self.notices:
            for tip in self.notices:
                self.aniPos(tip,
                            tip.pos(),
                            QPoint(tip.x(), tip.y()-tip.height()-self.spacing))
                # tip.move(tip.x(), tip.y()-tip.height()-self.spacing)

    # 动画
    def aniPos(self,obj,spos:QPoint,epos:QPoint):
        self.ani = QPropertyAnimation(self)
        self.ani.setTargetObject(obj)
        self.ani.setPropertyName(b"pos")
        self.ani.setStartValue(spos)
        self.ani.setEndValue(epos)
        self.ani.setDuration(100)
        self.ani.start()

    def appendTip(self,text:str,interval=3):
        tip = Notice(self.winp)
        tip.finish.connect(self.finish_event)
        tip.setText(text,interval*1000)
        if self.style:
            tip.setStyleSheet(self.style)
        self.notices.append(tip)
        self.notice_heights.append(QPoint(tip.x(),self.count()*tip.height()+self.spacing))
        print(self.notice_heights)
        if self.count()>1:
            # t_tip = self.notices[-1]
            self.aniPos(tip,QPoint(tip.x(),0),
                        self.notice_heights[self.count()-2])
            # tip.move(tip.x(), t_tip.y()+t_tip.height()+self.spacing)
        else:
            tip.move(tip.x(), 0)

        tip.show()

    def setStyleSheet(self,style:str):
        self.style = style