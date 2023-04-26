# -*- coding:utf-8 -*-
# @time:2023/4/269:39
# @author:LX
# @file:test_PageCuttingButtonGroup.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QStackedWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QButtonGroup,
    QPushButton,
    QSize,
    qt
)

from PyQtGuiLib.core import PageCuttingButtonGroup

'''
    PageCuttingButtonGroup 分页组件测试
'''

class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

        pageCount = 30
        buttonCount = 10

        self.setStyleSheet("""
                    QLabel{
                    font-size:30px;
                    }
                """)
        self.stackedWidget = QStackedWidget(self)
        for i in range(pageCount):
            page = QLabel("第{}页".format(i+1), self.stackedWidget)
            page.setAlignment(qt.AlignCenter)
            self.stackedWidget.addWidget(page)

        self.pbg = PageCuttingButtonGroup(pageCount, buttonCount)

        # 直接绑定 QStackedWidget
        self.pbg.bingStackedWidget(self.stackedWidget)

        self.pbg.setCurrentPageButtonFixedSize(QSize(34, 34))
        self.pbg.setPreviousNextPageButtonFixedSize(QSize(74, 34))
        self.pbg.setSpacing(8)

        hBox = QHBoxLayout()
        hBox.addWidget(self.pbg)
        vBox = QVBoxLayout()
        vBox.addWidget(self.stackedWidget)
        vBox.addLayout(hBox)
        vBox.setStretch(0, 1)
        self.setLayout(vBox)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())