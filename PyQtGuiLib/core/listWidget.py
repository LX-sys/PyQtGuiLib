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

        self.widgets = []

        # item的最小高度
        self.item_min_height = 150

    def setItemMinHeight(self,int):
        self.item_min_height = h

    # 添加 QWidget
    def addWidget(self,widget:QWidget):
        widget.setFixedHeight(self.item_min_height)

        item = ListWidgetItem()
        item.setSizeHint(QSize(self.width()-4,widget.height()))
        self.addItem(item)
        self.setItemWidget(item, widget)

        self.widgets.append((item,widget))