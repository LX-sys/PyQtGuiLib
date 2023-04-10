# -*- coding:utf-8 -*-
# @time:2023/4/1017:42
# @author:LX
# @file:listTemplateWindow.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QListWidgetItem,
    QIcon
)
import typing

from PyQtGuiLib.templateWindow.UI.listTemplateWindowUI import ListTemplateWindowUI


class ListTemplateWindow(ListTemplateWindowUI):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.addItem("dasdas")

    def addItem(self,text:typing.Union[str,QListWidgetItem],icon:str=None):
        if isinstance(text,QListWidgetItem):
            self.listWidget.addItem(text)
            return

        item = QListWidgetItem()
        item.setText(text)
        if icon:
            item.setIcon(QIcon(icon))
        self.listWidget.addItem(item)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = ListTemplateWindow()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
