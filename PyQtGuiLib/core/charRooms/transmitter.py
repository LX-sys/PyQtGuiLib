# -*- coding:utf-8 -*-
# @time:2023/6/116:49
# @author:LX
# @file:transmitter.py
# @software:PyCharm

from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QLineEdit,
    Qt,
    Signal,
    QFileDialog
)


class Transmitter(QWidget):
    texted = Signal(str)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setFixedHeight(80)

        self.vlay = QVBoxLayout(self)
        self.top_widget = QWidget()
        self.top_widget.setStyleSheet("border:2px solid red;")
        self.top_widget.hide()

        self.hlay = QHBoxLayout()
        self.hlay.setAlignment(Qt.AlignLeft)
        self.hlay.setSpacing(0)

        self.emo = QPushButton()
        self.emo.setFixedSize(40,40)
        self.emo.setText("😉")
        self.emo.setObjectName("emo")
        self.line = QLineEdit()
        self.line.setMinimumWidth(100)
        self.line.setFixedHeight(40)
        self.line.setPlaceholderText("输入消息")
        self.line.setObjectName("line")

        self.st = QStackedWidget()
        self.st.setFixedHeight(50)
        self.st.setMaximumWidth(200)
        # self.st.setStyleSheet("border:1px solid red;")
        self.ac_widget = QWidget()
        self.send_btn = QPushButton()
        self.send_btn.setText("发送")
        self.send_btn.setObjectName("send_btn")
        self.send_btn.setFixedSize(55,50)

        self.st.addWidget(self.ac_widget)
        self.st.addWidget(self.send_btn)

        self.hlay.addWidget(self.emo)
        self.hlay.addWidget(self.line)
        self.hlay.addWidget(self.st)

        self.vlay.addWidget(self.top_widget)
        self.vlay.addLayout(self.hlay)

        self.st.setCurrentIndex(0)
        self.acWidget()

        self.line.textChanged.connect(self.switchSt_event)

        self.send_btn.clicked.connect(self.sendEmit)
        self.line.returnPressed.connect(self.sendEmit)

        self.defaultStyle()

    def sendEmit(self):
        self.texted.emit(self.line.text())
        self.line.clear()

    def acWidget(self):
        self.st_hlay = QHBoxLayout(self.ac_widget)
        self.st_hlay.setAlignment(Qt.AlignLeft)

        self.file_dia = QPushButton()
        self.file_dia.setText("文")
        self.file_dia.setFixedSize(40,40)
        self.file_dia.setObjectName("file_dia")

        self.it_dia = QPushButton()
        self.it_dia.setText("...")
        self.it_dia.setFixedSize(40,40)
        self.it_dia.setObjectName("it_dia")

        self.st_hlay.addWidget(self.file_dia)
        self.st_hlay.addWidget(self.it_dia)

        self.file_dia.clicked.connect(self.file_event)

    def switchSt_event(self,text:str):
        if text:
            self.st.setCurrentIndex(1)
        else:
            self.st.setCurrentIndex(0)

    def file_event(self):
        file_name,file_type = QFileDialog.getOpenFileName(self,"文件")
        if file_name:
            print(file_name, file_type)

    def defaultStyle(self):
        self.setStyleSheet('''
*{
font: 11pt "等线";
}
#emo,#line,#file_dia,#it_dia{
border:none;
background-color:#fff;
}
#emo{
border-top-left-radius:20px;
border-bottom-left-radius:20px;
}
#line{
border-top-right-radius:20px;
border-bottom-right-radius:20px;
}
#file_dia,#it_dia{
border-radius:20%;
}
#send_btn:hover{
background-color: rgb(65, 130, 195);
}
#send_btn,#send_btn:pressed{
border-radius:20%;
border:none;
background-color:#55aaff;
margin-left:5px;
}

        ''')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Transmitter()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())