# -*- coding:utf-8 -*-
# @time:2023/5/269:53
# @author:LX
# @file:test_paletteDialog.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QColor
)

from PyQtGuiLib.core import PaletteTools

# QSplashScreen
'''
    测试用例的标准模板,该代码用于复制
'''


class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

        self.ptools = PaletteTools()
        self.ptools.show()
        self.ptools.clickColor.connect(self.updateColor)
        self.ptools.gradientQSSCoded.connect(self.updateGColor)

    def updateColor(self,color:QColor):
        self.setStyleSheet('''
        background-color: rgba({}, {}, {},{});
        '''.format(*color.getRgb()))

    def updateGColor(self,color_str):
        self.setStyleSheet("background-color:"+color_str)



if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())