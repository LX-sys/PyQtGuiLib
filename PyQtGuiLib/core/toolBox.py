# -*- coding:utf-8 -*-
# @time:2023/3/69:33
# @author:LX
# @file:toolBox.py
# @software:PyCharm

from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QToolBox,
    QWidget,
    QIcon,
    QListWidget,
    QListWidgetItem,
    QListView,
    QSize,
    QFont
)

class ToolBox(QToolBox):
    def __init__(self,*args,**kwargs):
        super().__init__()

        self.resize(300,300)
        self.setWindowTitle("ToolBox")
        self.layout().setSpacing(0)


        # item默认的图标大小
        self.default_item_icon_size = QSize(32, 32)

        self.addTextNode({
            "title":"page1",
            "icon":r"D:\code\PyQtGuiLib\tests\temp_image\python1.png",
            "item":{
                "text": "测试",
                "icon":r"D:\code\PyQtGuiLib\tests\temp_image\python1.png",
                "size":QSize(50,50)
            }
        })

        self.addTextNode({
            "title":"page1",
            "icon":r"D:\code\PyQtGuiLib\tests\temp_image\python1.png",
            "item":{
                "text": "测试",
                "icon":r"D:\code\PyQtGuiLib\tests\temp_image\python1.png",
                "size":QSize(50,50)
            }
        })


    def addTextNode(self,data:dict):
        '''
            {
                "title":""
                "icon":None,
                "item":{
                    "icon":None,
                    "text":"",
                    "size":QSize() or None
                }
            }

        :param data:
        :return:
        '''
        title_text = data.get("title")
        title_icon = data.get("icon")
        item_icon = data.get("item").get("icon")
        item_text = data.get("item").get("text")
        item_size = data.get("item").get("size")
        print(item_size)

        node = QListWidget()
        if item_size:
            node.setIconSize(item_size)
        else:
            node.setIconSize(self.default_item_icon_size)
        item_node = QListWidgetItem()
        item_node.setText(item_text)
        if item_icon:
            item_node.setIcon(QIcon(item_icon))
        node.addItem(item_node)

        if title_icon:
            self.addItem(node,QIcon(title_icon),title_text)
        else:
            self.addItem(node,title_text)



    # def addItem(self, item: QWidget, text: str,icon:QIcon=None) -> int:
    #
    #     if icon:
    #         super(ToolBox, self).addItem(item,icon,text)
    #     else:
    #         super(ToolBox, self).addItem(item, text)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = ToolBox()
    win.show()

    sys.exit(app.exec_())