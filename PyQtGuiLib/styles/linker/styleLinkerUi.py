# -*- coding:utf-8 -*-
# @time:2023/2/1817:13
# @author:LX
# @file:styleLinkerUi.py
# @software:PyCharm
from PyQtGuiLib.header import (
    QWidget,
    QTabWidget,
    qt,
    QTreeWidget,
    QHBoxLayout,
    QSplitter,
    QTextBrowser
)


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
        self.defaultPage = QTextBrowser()
        self.__tab.addTab(self.defaultPage,"样式代码")

        self.__spliter.addWidget(self.__tree)
        self.__spliter.addWidget(self.__tab)
        self.__spliter.setStretchFactor(1,8)

    def browser(self)->QTextBrowser:
        return self.defaultPage

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