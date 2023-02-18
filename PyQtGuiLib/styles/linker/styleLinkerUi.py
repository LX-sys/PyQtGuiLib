# -*- coding:utf-8 -*-
# @time:2023/2/1817:13
# @author:LX
# @file:styleLinkerUi.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QPushButton,
    QLabel,
    QTabWidget,
    QObject,
    qt,
    QGroupBox,
    QTreeWidget,
    QHBoxLayout,
    QSplitter
)
from PyQtGuiLib.styles import QssStyleAnalysis
from PyQtGuiLib.core import PaletteFrame


class StyleLinkerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800,600)

        self.setWindowTitle("动态样式链接器")

        self.Init()


    def Init(self):
        self.__hboy = QHBoxLayout(self)
        self.__hboy.setContentsMargins(0,0,0,0)
        self.__spliter = QSplitter()
        self.__hboy.addWidget(self.__spliter)

        self.__tree = QTreeWidget()
        self.__tree.header().setVisible(False)
        self.__tab = QTabWidget()
        self.defaultPage = QWidget()
        self.__tab.addTab(self.defaultPage,"样式代码")

        self.__spliter.addWidget(self.__tree)
        self.__spliter.addWidget(self.__tab)
        self.__spliter.setStretchFactor(1,8)

    def tree(self)->QTreeWidget:
        return self.__tree

    def tab(self)->QTabWidget:
        return self.__tab


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = StyleLinkerUI()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())