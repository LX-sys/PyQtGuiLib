# -*- coding:utf-8 -*-
# @time:2023/4/2817:23
# @author:LX
# @file:table.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    qt,
    Qt,
    QPushButton
)

from typing import List,Optional


class HeaderItem(QPushButton):
    def __init__(self,text:str):
        super().__init__()
        self.setText(text)

        self.setStyleSheet('''
        border:none;
        ''')


class Table(QTableWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)

        self.setGrid(5,5)
        self.setHeaderLabels(["A","B","C","D"],True)

    def setHeaderLabels(self,labels:List[str],center=False):
        for i,label in enumerate(labels):
            item = HeaderItem(label)
            self.setCellWidget(0,i,item)

    def setGrid(self,row:int,col:int):
        self.setRowCount(row)
        self.setColumnCount(col)

    def gridSize(self)->tuple:
        return self.rowCount(),self.columnCount()



if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Table()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())