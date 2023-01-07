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


    def addWidget(self,widget:QWidget):
        item = ListWidgetItem()
        item.setSizeHint(QSize(self.width(),widget.height()))
        # self.setItemDelegate(ItemDelegate())
        self.addItem(item)
        self.setItemWidget(item, widget)
