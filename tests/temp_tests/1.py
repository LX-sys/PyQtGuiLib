import sys
from PyQt5.QtWidgets import QWidget, QApplication,QVBoxLayout,QFrame,QPushButton
from PyQt5.QtGui import QBitmap, QPainter, QColor
from PyQt5.QtCore import Qt,QSize

class MyWidget(QFrame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # 创建一个圆形掩码
        # self.mask = QBitmap(self.size())
        # self.mask.fill(Qt.black)

        self.setStyleSheet('''
        background-color: rgb(85, 170, 127);
        border:2px solid yellow;
        ''')


    def paintEvent(self, e) -> None:
        self.mask = QBitmap(self.size())
        self.mask.fill(Qt.black)
        painter = QPainter(self.mask)
        painter.setBrush(QColor(Qt.white))
        painter.drawEllipse(-15, -15, 90, 90)
        # painter.setPen(Qt.green)
        # painter.setBrush(QColor(Qt.green))
        # painter.drawRect(0,0,30,30)
        # self.mask.
        self.setMask(self.mask)

        painter.end()



class Test(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800,600)
        self.boy = QVBoxLayout(self)
        self.widget = MyWidget()
        self.boy.addWidget(self.widget)

        self.btn = QPushButton("按钮",self)
        self.btn.resize(80,80)
        self.btn.setStyleSheet('''
        QPushButton{
background-color: rgb(8, 8, 8);
border:2px solid #8cfff7;
color:rgb(220, 220, 220);
border-radius:40px;
}
QPushButton:hover{
background-color: rgb(0, 0, 0);
}
QPushButton:pressed{
background-color:rgb(50, 50, 50);
}
        ''')



# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     widget = Test()
#     widget.show()
#     app.exec_()
