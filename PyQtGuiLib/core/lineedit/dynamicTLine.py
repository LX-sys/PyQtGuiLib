from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QPainter,
    QPropertyAnimation,
    QPoint,
    QSize,
    QRect,
    QPaintEvent,
    qt,
    QLineEdit,
    QLabel,
    Signal,
    QFont,
    textSize
)

'''
    动态 标题输入框
'''
class LineEdit(QLineEdit):
    # 聚焦信号
    focused = Signal(bool)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # 默认不聚焦
        self.setFocusPolicy(qt.ClickFocus)

    def focusInEvent(self, ev) -> None:
        self.focused.emit(True)
        super().focusInEvent(ev)

    def focusOutEvent(self,ev) -> None:
        self.focused.emit(False)
        super().focusOutEvent(ev)


class DynamicTLine(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.w,self.h = 240,70


        # 样式表生效
        self.setAttribute(qt.WA_StyledBackground,True)

        # 提示文字
        self.placeholderText = "User"

        # 标题文本和输入文本
        self.title_text = self.placeholderText
        self.input_text = ""

        # 标题文字大小
        f = QFont(self.title_text)
        fs = textSize(f,self.title_text)
        self.title_size = QSize(fs.width(),fs.width())

        # 标题的区域范围
        self.t_w,self.t_h = 240,self.title_size.height()

        # 输入的区域范围
        self.input_w, self.input_h = 240, self.h - self.t_h - 1

        # --
        self.title = QLabel(self)
        self.input = LineEdit(self)
        self.input.focused.connect(self.focus_event)

        self.input.setStyleSheet('''
border:none;
border-bottom:2px solid rgb(85, 0, 255);
background-color: transparent;    
    ''')

        self.Init()

        self.resize(self.w, self.h)

    # 聚焦事件
    def focus_event(self, b:bool):
        if self.input.text():
            return

        ani = QPropertyAnimation(self.title)
        ani.setTargetObject(self.title)
        ani.setPropertyName(b"pos")
        ani.setDuration(300)

        def _t(self,b):
            self.input.show()
            self.input.setPlaceholderText("")
            if not b:
                self.title.hide()
                self.input.setPlaceholderText(self.placeholderText)

        ani.finished.connect(lambda: _t(self,b))

        if b:
            y = self.input.height()//2+10
            self.title.move(5,y)
            self.input.setPlaceholderText("")
            self.title.setText(self.placeholderText)
            self.title.show()
            # 动画
            ani.setStartValue(self.title.pos())
            ani.setEndValue(QPoint(0,0))
        else:
            self.title.show()
            ani.setStartValue(self.title.pos())
            ani.setEndValue(QPoint(self.input.x()+2,self.input.y()))

        ani.start()

    def Init(self):
        self.title.setGeometry(0, 0, self.t_w, self.t_h)
        self.title.hide()
        self.input.setGeometry(0,self.t_h-1,self.input_w,self.input_h)

        self.setPlaceholderText(self.placeholderText)

    # 设置提示文字
    def setPlaceholderText(self,text):
        self.placeholderText = text
        self.input.setPlaceholderText(self.placeholderText)
        self.title.setText(self.placeholderText)

    # 获取文本
    def text(self)->str:
        return self.input.text()

    # 标题对象
    def label(self)->QLabel:
        return self.title

    # 输入框对象
    def line(self)->QLineEdit:
        return self.input

    def updateSize(self):
        self.title.resize(self.width(),self.title.height())
        self.input.resize(self.width(),self.height()-self.title.height())

    def paintEvent(self, e:QPaintEvent) -> None:
        painter = QPainter(self)

        self.updateSize()

        painter.end()
