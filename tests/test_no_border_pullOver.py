# -*- coding:utf-8 -*-
# @time:2022/12/2910:07
# @author:LX
# @file:test_no_border_pullOver.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QPushButton
)

from PyQtGuiLib.core import PullOver
from PyQtGuiLib.core.widgets import BorderlessWidget
'''
    无边框窗口 + 窗口停靠 组合功能
'''

class TestCombination(BorderlessWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800,500)

        self.setStyleSheet('''
#widget{
background-color:#d4d4d4;
border-radius:30px;
}
        ''')

        self.show_btn = QPushButton()
        self.show_btn.resize(70, 70)
        self.show_btn.setObjectName("show_btn")
        self.show_btn.setStyleSheet('''
                #show_btn{
                background-color:green;
                border-radius:35px;
                }
                ''')

        # 窗口靠边功能
        self.pullOver = PullOver(self)
        # self.pullOver.setEasingCurve(PullOver.OutBounce)
        self.pullOver.pullover(self.show_btn)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TestCombination()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())