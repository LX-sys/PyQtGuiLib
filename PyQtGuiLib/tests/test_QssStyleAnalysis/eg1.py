# -*- coding:utf-8 -*-
# @time:2023/2/914:20
# @author:LX
# @file:eg1.py
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
    QFrame,
    QStyleOption,
    QPainter,
    QStyle
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

        # 创建一个针对整个窗口的 QSS 解析器
        self.qss = QssStyleAnalysis(self)
        # 对窗口上所有按钮,标签设置样式
        self.qss.setQSS('''
        QPushButton{
        color: rgb(0, 255, 127);
        background-color:rgb(0, 170, 0);
        }
        QLabel{
        color: rgb(42, 55, 127);
        background-color:rgb(255, 170, 0);
        }
        ''')
        # print(self.qss.toStr()) # 返回样式的原始的类型
        # print(self.qss.toDict()) # 返回样式的字典类型
        # print("----------------------------------------------------")
        # print(self.qss.selector("QPushButton").header()) # 获取按钮的选择器
        # print(self.qss.selector("QPushButton").headerSubdivision()) # 在有多个选择器的这个才能看到效果
        # print(self.qss.selector("QPushButton").body()) # 获取该选择器的原始样式
        # print(self.qss.selector("QPushButton").bodySubdivision()) # 将原始样式已列表的形式返回
        # print(self.qss.selector("QPushButton").bodyToDict()) # 将原始样式已字典的形式返回(不带选择器)
        # print(self.qss.selector("QPushButton").toDict()) # 将原始样式已字典的形式返回(带选择器)
        # print(self.qss.selector("QPushButton").attr("color")) # 获取该选择器下面某个属性的值
        self.qss.selector("QPushButton").updateAttr("background-color","red") # 修改背景样式


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())