from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    qt,
    QPushButton,
    QLabel,
    Qt,
)

from PyQtGuiLib.styles import QssStyleAnalysis


class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)


        self.setAttribute(Qt.WA_StyledBackground,True)

        self.l = QLabel("测试标签",self)
        self.btn = QPushButton("测试按钮",self)
        self.btn.setObjectName("btn")
        self.btn2 = QPushButton("测试按钮2号",self)
        self.l.move(30, 30)
        self.btn.resize(150, 80)
        self.btn.move(80, 80)
        self.btn2.resize(100,60)
        self.btn2.move(250,80)

        '''
            解析 测试1 
        '''

        # 创建一个针对 测试按钮 的QSS解析器
        self.qss = QssStyleAnalysis(self.btn)
        # 对窗口上所有按钮,标签设置样式
        self.qss.setQSS('''
        QPushButton{
        color: rgb(0, 255, 127);
        background-color:rgb(0, 170, 0);
        }
        ''')

        # 重新创建一个针对 测试按钮 的QSS解析器
        # 通过 inherit() 可以将'测试按钮'的样式 传承到 '测试按钮2号' 上
        self.btnqss = QssStyleAnalysis(self.btn)
        self.btnqss.inherit()
        self.btnqss.setParent(self.btn2) # 关键语句

        print(self.btnqss.toStr())
        self.btnqss.selector("QPushButton").updateAttr("color","blue")
        self.btnqss.appendQSSDict({
          "QPushButton:hover":{
              "border":"1px solid blue"
          }
        })


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())