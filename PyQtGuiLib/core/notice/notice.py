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
    QObject,

)


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

    U_Center = "U_Center"
    Left_Down= "Left_Down"
    Rigth_Down = "Rigth_Down"

    def __init__(self,parent=None):
        super().__init__(parent)
        self.resize(220,40)
        self.__parent = parent

        self.setWindowFlags(qt.FramelessWindowHint|qt.WindowStaysOnTopHint|qt.WindowTransparentForInput)
        self.setAttribute(qt.WA_TranslucentBackground,True)

        self.__text = "hello wrold"
        self.__pos = Notice.U_Center

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

    def appendText(self,str):
        pass

    def updatePos(self):
        w = self.__parent.width()
        h = self.__parent.height()

        if self.__pos == Notice.Left_Down:
            self.move(self.get_margin(),h-self.height()-self.get_margin()*2)
        elif self.__pos == Notice.Rigth_Down:
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

        self.style = ""

    def count(self)->int:
        return len(self.notices)

    def finish_event(self,obj:QObject):
        self.notices.remove(obj)
        print(self.notices)
        # 未写完
        for wid in self.notices:
            x, y = wid.x(), wid.y()
            wid.move(x,y-(self.count()-1)*wid.height()+5)
        self.winp.update()

    def appendTip(self,text:str,interval=3000):
        tip = Notice(self.winp)
        tip.finish.connect(self.finish_event)
        tip.setText(text,interval)
        if self.style:
            tip.setStyleSheet(self.style)
        self.notices.append(tip)
        print(self.count())
        x,y = tip.x(),tip.y()

        tip.move(x,y+(self.count()-1)*tip.height()+5)
        tip.show()

    def setStyleSheet(self,style:str):
        self.style = style

    def show(self):
        w = self.winp.width()
        h = self.winp.height()

        for wid in self.notices:
            try:
                if wid is None:
                    print("wid:",wid)
                # else:
                #     print()
            except Exception as e:
                print(e)

        y = 0

        for wid in self.notices:
            print(wid)
            try:
                wid.move(w // 2 - wid.width() // 2, wid.get_margin()+y)
                y+=wid.height()+wid.get_margin()*2
                wid.show()
            except:
                pass
