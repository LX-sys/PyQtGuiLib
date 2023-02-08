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
    Qt,
    QPalette,
    QColor,
    QPaintEvent,
    QPainter,
    QBrush,
    QSize,
    QMainWindow,
    QLineEdit,
    desktopCenter,
    QPixmap,
    QLinearGradient,
    QLabel,
    QFont,
    textSize,
    QFontMetricsF,
    Qt
)

from PyQtGuiLib.styles import QssStyleAnalysis


class Test(QMainWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)



        self.btn = QPushButton("测试按钮",self)

        # QSS 解析器
        self.qss = QssStyleAnalysis(self.btn)
        self.qss.setQSS('''
        QPushButton{
        	color: rgb(0, 255, 127);
        	background-color:rgb(0, 170, 0);
        }''')
        self.qss.qss("QPushButton").updateAttr("color","red")



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