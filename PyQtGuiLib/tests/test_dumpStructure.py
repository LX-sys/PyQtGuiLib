

'''
    测试 控件的组成分析函数
'''


from PyQtGuiLib.core.resolver import dumpStructure

import sys
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QTabWidget,QScrollArea,QCheckBox,QDialog


app = QApplication(sys.argv)
dumpStructure(QDialog())

