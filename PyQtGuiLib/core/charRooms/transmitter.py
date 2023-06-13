# -*- coding:utf-8 -*-
# @time:2023/6/116:49
# @author:LX
# @file:transmitter.py
# @software:PyCharm

from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    is_win_sys,
    is_mac_sys,
    sys,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QLineEdit,
    Qt,
    Signal,
    QFileDialog,
    QTextEdit,
    QDragEnterEvent,
    QDropEvent
)


class MesLineEdit(QLineEdit):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e:QDragEnterEvent) -> None:
        e.accept()

    def dropEvent(self, e:QDropEvent) -> None:
        file_path = e.mimeData().text()  # type:str
        if is_win_sys:
            file_path = file_path.replace("file:/","")
        print("event:",file_path)


class Transmitter(QWidget):
    texted = Signal(str)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setFixedHeight(80)

        self.vlay = QVBoxLayout(self)
        self.top_widget = QWidget()
        self.top_widget.setStyleSheet("border:2px solid red;")
        self.top_hlay = QHBoxLayout(self.top_widget)

        self.hlay = QHBoxLayout()
        self.hlay.setAlignment(Qt.AlignLeft)
        self.hlay.setSpacing(0)

        self.emo = QPushButton()
        self.emo.setFixedSize(40,40)
        self.emo.setText("😉")
        self.emo.setObjectName("emo")
        self.line = MesLineEdit()
        self.line.setMinimumWidth(100)
        self.line.setFixedHeight(40)
        self.line.setPlaceholderText("输入消息")
        self.line.setObjectName("line")

        self.st = QStackedWidget()
        self.st.setFixedHeight(50)
        self.st.setMaximumWidth(200)
        self.ac_widget = QWidget()
        self.btn_widget = QWidget()

        self.st.addWidget(self.ac_widget)
        self.st.addWidget(self.btn_widget)

        self.hlay.addWidget(self.emo)
        self.hlay.addWidget(self.line)
        self.hlay.addWidget(self.st)

        self.vlay.addWidget(self.top_widget)
        self.vlay.addLayout(self.hlay)

        self.st.setCurrentIndex(0)
        self.acWidget()
        self.sendWidget()

        self.line.textChanged.connect(self.switchSt_event)
        self.line.returnPressed.connect(self.sendEmit)

        self.defaultStyle()

    def sendEmit(self):
        self.texted.emit(self.line.text())
        self.line.clear()

    def acWidget(self):
        self.st_hlay = QHBoxLayout(self.ac_widget)
        self.st_hlay.setContentsMargins(9,0,0,0)
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

    def sendWidget(self):
        self.send_hlay = QHBoxLayout(self.btn_widget)
        self.send_hlay.setContentsMargins(9,0,0,0)
        self.send_hlay.setAlignment(Qt.AlignLeft)

        self.send_btn = QPushButton()
        self.send_btn.setText("发送")
        self.send_btn.setObjectName("send_btn")
        self.send_btn.setFixedSize(40,40)

        self.send_hlay.addWidget(self.send_btn)

        self.send_btn.clicked.connect(self.sendEmit)

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
border-top-left-radius:10%;
border-bottom-left-radius:10%;
}
#line{
border-top-right-radius:10%;
border-bottom-right-radius:10%;
}
#file_dia,#it_dia{
border-radius:10%;
}
#send_btn:hover{
background-color: rgb(65, 130, 195);
}
#send_btn,#send_btn:pressed{
border-radius:10%;
border:none;
background-color:#55aaff;
font: 10pt "等线";
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