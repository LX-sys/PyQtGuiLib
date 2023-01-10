from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QListWidget,
    QListWidgetItem,
    QWidget,
    QSize,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QModelIndex
)

from PyQtGuiLib.core.resolver import dumpStructure

'''

    QListWidget 增强版本
'''

class ItemDelegate(QStyledItemDelegate):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def updateEditorGeometry(self, editor:QWidget, option:QStyleOptionViewItem, index:QModelIndex) -> None:
        editor.setGeometry(option.rect)


class ListWidgetItem(QListWidgetItem):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)


class ListWidget(QListWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        # 存储(item,widget)
        self.widgets = []

        # item的最小高度
        self.item_min_height = 30
        self.defaultStyle()

    # 设置item的最小高度
    def setItemMinHeight(self,h:int):
        self.item_min_height = h

    def addItem(self, aitem: QListWidgetItem) -> None:
        super().addItem(aitem)

    # 添加 QWidget
    def addWidget(self,widget:QWidget):
        widget.setFixedHeight(self.item_min_height)

        item = ListWidgetItem()
        item.setSizeHint(QSize(self.width()-4,widget.height()))
        self.addItem(item)
        self.setItemWidget(item, widget)

        self.widgets.append((item,widget))

    # 默认样式
    def defaultStyle(self):
        if not self.styleSheet():
            self.setStyleSheet('''
QListWidget{
border:none;
background-color:#d6d6d6;
}
QListWidget QScrollBar{
background-color: #d9d9d9;
width:12px;
}
      ''')

    # 返回所有窗口
    def getAllWidget(self) -> list:
        return [wid[1] for wid in self.widgets]

    # 移除窗口
    def removeWidget(self,widget:QWidget):
        if not widget:
            return

        for i,ws in enumerate(self.widgets):
            item,wid = ws
            if wid == widget:
                self.widgets.remove(ws)
                self.removeItemWidget(item)
                wid.deleteLater()
                self.takeItem(i)
                del item
                break