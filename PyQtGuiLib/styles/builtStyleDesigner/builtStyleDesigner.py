# -*- coding:utf-8 -*-
# @time:2023/1/87:12
# @author:LX
# @file:builtStyleDesigner.py
# @software:PyCharm


from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QVBoxLayout,
    QResizeEvent,
    QTreeWidgetItem,
    QWidget,
    QSize,
    QPushButton,
    QColorDialog
)
from functools import partial
from PyQtGuiLib.styles.builtStyleDesigner.builtStyleDesignerUI import BuiltStyleDesignerUI
from PyQtGuiLib.styles import ButtonStyle
'''

    内置-样式设计器
'''

class BuiltStyleDesigner(BuiltStyleDesignerUI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(1100, 850)

        self.addTree({
            "QPushButton":[("randomStyle","随机样式"),
                           ("contrastStyle","互补色样式"),
                           ("homologyStyle","同色调样式")]
                      })

        # 判断是否已经创建的控件,控件列表,控件数量
        self.is_Controls = False
        self.controls = []
        self.control_number = 35

        # 当前点击的控件名称,方法
        self.cu_click_name = ""
        self.cu_fun = ""

        # ----------
        # 设置一个当前的控件数量
        self.c_number_spin.setValue(self.control_number)

        self.myEvent()

    # 添加控件
    def addControls(self,widget:QWidget,size:QSize=QSize(130,60)):
        widget.setFixedSize(size)
        self.flow.addWidget(widget)

    def addTree(self,tree_dict:dict):
        if not tree_dict:
            return None

        tree = self.treeObj()

        for name,values in tree_dict.items():
            item = QTreeWidgetItem(tree)
            item.setText(0, name)
            for ch,explain in values:
                item_c = QTreeWidgetItem(item)
                item_c.setText(0, ch)
                item_c.setText(1, explain)
                # tree.addTopLevelItem(item)

    def itemDoubleClick_event(self,item:QTreeWidgetItem,column:int):
        text = item.text(column)

        if text[0] == "Q":
            print("父节点:",text)
            if text == "QPushButton":
                if not self.is_Controls:

                    # 设置
                    self.is_Controls = True
                    self.cu_fun = "randomStyle"
                    self.cu_click_name = "QPushButton"

                    for i in range(self.control_number):
                        btn = QPushButton()
                        btn.setText("test_{}".format(i))
                        btn.setStyleSheet(ButtonStyle.randomStyle())
                        btn.clicked.connect(partial(self.qss_event,btn.styleSheet()))
                        self.controls.append(btn)
                        self.addControls(btn)
                else:
                    self.is_Controls = False
                    for w in self.controls:
                        self.flow.removeWidget(w)
                    self.controls.clear()

        else:
            print("子节点:",text)
            if not self.controls:
                return

            # 设置
            self.cu_fun = text

            for w in self.controls:
                if self.cu_click_name == "QPushButton":
                    if text == "randomStyle":
                        w.setStyleSheet(ButtonStyle.randomStyle())
                    elif text == "contrastStyle":
                        w.setStyleSheet(ButtonStyle.contrastStyle())
                    elif text == "homologyStyle":
                        w.setStyleSheet(ButtonStyle.homologyStyle())

    # 控件数量改变事件
    def number_event(self,n:int):
        if not self.controls:
            self.control_number = n
            return

        if n > self.control_number:
            if self.cu_click_name == "QPushButton":
                btn = QPushButton()
                btn.setText("hello")
                self.controls.append(btn)

                if self.cu_fun == "randomStyle":
                    btn.setStyleSheet(ButtonStyle.randomStyle())
                elif self.cu_fun == "contrastStyle":
                    btn.setStyleSheet(ButtonStyle.contrastStyle())
                elif self.cu_fun == "homologyStyle":
                    btn.setStyleSheet(ButtonStyle.homologyStyle())

                btn.clicked.connect(partial(self.qss_event, btn.styleSheet()))
                self.addControls(btn)
        else:
            pop = self.controls.pop(-1)
            pop.clicked.disconnect()
            self.flow.removeWidget(pop)
        self.control_number = n

    # qss代码事件
    def qss_event(self,qss:str):
        self.qssEditObj().clear()
        self.qssEditObj().setText(qss)

    # 修改背景颜色事件
    def background_color_event(self):
        rgb_obj = QColorDialog.getColor()
        rgb = rgb_obj.getRgb()
        self.back_c_btn.setStyleSheet("background-color:rgb({},{},{},{})".format(*rgb))
        self.showObj().setStyleSheet("background-color:rgb({},{},{},{})".format(*rgb))

    def myEvent(self):
        self.treeObj().itemDoubleClicked.connect(self.itemDoubleClick_event)

        self.c_number_spin.valueChanged.connect(self.number_event)
        self.back_c_btn.clicked.connect(self.background_color_event)


    def resizeEvent(self, e:QResizeEvent) -> None:
        self.updateSize()
        super().resizeEvent(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = BuiltStyleDesigner()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())