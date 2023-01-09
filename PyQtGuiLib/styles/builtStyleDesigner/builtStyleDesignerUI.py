# -*- coding:utf-8 -*-
# @time:2023/1/87:03
# @author:LX
# @file:builtStyleDesignerUI.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QFrame,
    QTreeWidget,
    QSplitter,
    qt,
    QTabWidget,
    QTextEdit,
    QSpinBox,
    QFormLayout,
    QLabel,
    QPushButton,
    QScrollArea
)

'''

    内置-样式设计器 UI 界面
'''

from PyQtGuiLib.core.widgets import BorderlessFrame,TitleBar
from PyQtGuiLib.core import FlowLayout


class BuiltStyleDesignerUI(BorderlessFrame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(1100,850)
        self.setObjectName("BuiltStyleDesigner")
        self.InitWidget()

    def InitWidget(self):
        self.setStyleSheet('''
#BuiltStyleDesigner{
background-color:#d4d4d4;
}
#top_rigth_show{
border:2px solid blue;
}
#bottom_left_qss{
font-size:16px;
}
        ''')

        # 创建标题栏
        self.titbar = TitleBar(self)
        self.titbar.setBtnStyle(TitleBar.MacStyle)
        self.titbar.setTitleText("内置-样式设计器")

        # 创建上下布局
        self.sp_vlay = QSplitter(self)
        self.sp_vlay.setHandleWidth(2)
        self.sp_vlay.setGeometry(0,self.titbar.height(),self.size().width(),self.size().height())
        self.sp_vlay.setOrientation(qt.Vertical)

        self.top_widget = QWidget()
        self.bottom_widget = QWidget()

        self.top_widget.setObjectName("top_widget")
        self.bottom_widget.setObjectName("bottom_widget")

        self.sp_vlay.addWidget(self.top_widget)
        self.sp_vlay.addWidget(self.bottom_widget)
        self.sp_vlay.setSizes([self.height()-300,300])

        # 在上布局的QWidget布局
        self.top_hlay = QHBoxLayout(self.top_widget)
        self.top_left_tree = QTreeWidget()
        self.top_left_tree.setColumnCount(2)
        self.top_left_tree.setHeaderLabels(["组件","方法"])
        self.top_left_tree.setMaximumWidth(300)

        self.top_rigth_show = QScrollArea()
        self.top_rigth_show_core = QFrame()
        self.top_rigth_show.setWidget(self.top_rigth_show_core)
        self.top_rigth_show.setWidgetResizable(True)
        self.flow = FlowLayout(self.top_rigth_show_core)
        self.top_left_tree.setObjectName("top_left_tree")
        self.top_rigth_show_core.setObjectName("top_rigth_show")

        self.top_hlay.addWidget(self.top_left_tree)
        self.top_hlay.addWidget(self.top_rigth_show)

        # 在下布局的QWidget布局
        self.sp_hlay = QSplitter(self.bottom_widget)
        self.sp_hlay.setContentsMargins(9,0,9,5)
        self.sp_hlay.setHandleWidth(2)
        self.sp_hlay.setGeometry(0, 0, self.bottom_widget.width(), self.bottom_widget.height()-self.titbar.height())
        self.sp_hlay.setOrientation(qt.Horizontal)

        self.bottom_left_tab = QTabWidget()
        self.bottom_left_qss = QTextEdit()
        self.bottom_left_tab.setObjectName("bottom_left_tab")
        self.bottom_left_qss.setObjectName("bottom_left_qss")

        self.sp_hlay.addWidget(self.bottom_left_tab)
        self.sp_hlay.addWidget(self.bottom_left_qss)
        self.sp_hlay.setSizes([self.height() - 300, 300])

        # 创建控制台
        self.consoleTab()

        self.sp_vlay.splitterMoved.connect(self.updateSize)

    # 控制台
    def consoleTab(self):
        self.console_widget = QWidget()
        self.bottom_left_tab.addTab(self.console_widget,"控制台")

        # 表单布局
        self.form_lay = QFormLayout(self.console_widget)

        self.c_number_l = QLabel("控件数量")
        self.c_number_spin = QSpinBox()
        self.c_number_spin.setMinimum(1)
        self.c_number_spin.setMaximum(60)

        self.back_c_l = QLabel("背景颜色")
        self.back_c_btn = QPushButton("颜色")

        # self.c_size_l = QLabel("控件大小")
        # self.c_size_l = QPushButton("颜色")

        self.form_lay.addRow(self.c_number_l,self.c_number_spin)
        self.form_lay.addRow(self.back_c_l,self.back_c_btn)

    def updateSize(self):
        self.sp_vlay.setGeometry(0, self.titbar.height(), self.size().width(), self.size().height())
        self.sp_hlay.setGeometry(0, 0, self.bottom_widget.width(), self.bottom_widget.height()-self.titbar.height())

    def treeObj(self)->QTreeWidget:
        return self.top_left_tree

    def showObj(self)->QFrame:
        return self.top_rigth_show_core

    def tabObj(self)->QTabWidget:
        return self.bottom_left_tab

    def qssEditObj(self)->QTextEdit:
        return self.bottom_left_qss

    def flowObj(self)->FlowLayout:
        return self.flow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = BuiltStyleDesignerUI()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())