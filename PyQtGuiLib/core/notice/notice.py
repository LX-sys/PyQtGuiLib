from PyQtGuiLib.header import (
    QWidget,
    CustomStyle,
    QPainter,
    QBrush,
    QColor,
    QKeyEvent,
    QFont,
    QPaintEvent,
    qt,
    Qt,
    textSize,
    QThread,
    Signal,
    QPen,
    QGraphicsDropShadowEffect,
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
class Notice(QWidget,CustomStyle):
    U_Center = "U_Center"
    Left_Down= "Left_Down"
    Rigth_Down = "Rigth_Down"

    def __init__(self,parent=None):
        super().__init__(parent)
        self.resize(250,50)
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

        try:
            if self.__pos == Notice.Left_Down:
                self.move(self.get_margin(),h-self.height()-self.get_margin()*2)
            elif self.__pos == Notice.Rigth_Down:
                self.move(w-self.width()-self.get_margin(),h-self.height()-self.get_margin()*2)
            else:
                self.move(w//2-self.width()//2,self.get_margin())
        except:
            pass

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

        # self.updatePos()
        painter.end()

    def closeEvent(self, event) -> None:
        super().closeEvent(event)


class Notices:
    def __init__(self,parent:QWidget):
        self.winp = parent

        # 通知组
        self.notices = []

    def appendTip(self,text:str,interval=3000):
        tip = Notice(self.winp)
        tip.setText(text,interval)
        self.notices.append(tip)

    def setStyleSheet(self,style:str):
        for wid in self.notices:
            wid.setStyleSheet(style)

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
