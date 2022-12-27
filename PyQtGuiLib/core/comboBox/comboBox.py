# -*- coding:utf-8 -*-
# @time:2022/12/2716:00
# @author:LX
# @file:comboBox.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QWidget,
    QThread,
    Signal,
    QLineEdit,
    QInputMethodEvent,
    QKeyEvent,
    QPaintEvent,
    QPainter,
    QPen,
    QFont
)


'''
    传统下拉框
'''

class ComboBox(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.w,self.h = 400,300

        self.resize(self.w,self.h)

        self.text = ""

        # self.lineedit = QLineEdit(self)
        # self.lineedit.move(0,0)
        # self.lineedit.resize(self.w,50)
        # self.lineedit.setEnabled(False)

        self.createClickArea()

    # 创建点击区域
    def createClickArea(self):
        pass

    
    def keyPressEvent(self, e: QKeyEvent) -> None:
        print(e.key())
        if e.key() == 16777219:
            self.text = self.text[:-1]
        else:
            self.text += e.text()
        self.update()
        super().keyPressEvent(e)

    def paintEvent(self, e: QPaintEvent) -> None:
        painter = QPainter(self)

        font = QFont()
        font.setPointSize(15)
        painter.setFont(font)

        painter.drawLine(8,0,8,40)
        painter.drawRect(0,0,self.w,50)

        painter.drawText(10,25,self.text)

        painter.end()
    # def inputMethodEvent(self, e: QInputMethodEvent) -> None:
    #     print(e)
    #     super(ComboBox, self).inputMethodEvent(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ComboBox()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())