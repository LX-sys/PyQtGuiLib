# -*- coding:utf-8 -*-
# @time:2023/2/818:14
# @author:LX
# @file:test_QssStyleAnalysis.py
# @software:PyCharm


from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    qt,
    QPushButton,
    QLabel,
    Qt,
    QMainWindow,
    QPainterPath
)

from PyQtGuiLib.styles import QssStyleAnalysis


class Test(QMainWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

        self.l = QLabel("测试标签",self)
        self.btn = QPushButton("测试按钮",self)

        # QSS 解析器
        self.qss = QssStyleAnalysis(self)
        self.qss.setQSS('''
        QPushButton{
        color: rgb(0, 255, 127);
        background-color:rgb(0, 170, 0);
        }
        QPushButton:hover{
        }
        ''')
        self.qss.appendQSSDict({
            "QLabel":{
                "border":"2px solid yellow"
            }
        })
        self.qss.selector("QPushButton:hover").updateAttr("border", "2px solid blue")

        self.l.move(30, 30)
        self.btn.resize(150,80)
        self.btn.move(80,80)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())