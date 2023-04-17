# -*- coding:utf-8 -*-
# @time:2023/4/158:55
# @author:LX
# @file:listTree.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QPainter,
    QFont,
    QColor,
    QSize,
    QPaintEvent,
    QRect,
    Qt,
    textSize,
    QPoint,
    QToolButton,
    QAction,
    QMenu,
    Qt
)



class ListTree(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(300,600)

        # 默认节点高度
        self.__item_height = 55
        self.__margin = 5

        self.__items = [
            {"bg":{
            "rect": QRect(5, 5, -1, 50)
           },
           "text":{
                "text":"hello",
               "pos":QPoint(-1,25)
        }},
            {"bg":{
            "rect": QRect(5,5*2+50,-1,50)
           },
           "text":{
                "text":"hello",
               "pos":QPoint(-1,75)
        }}]

    def count(self)->int:
        return len(self.__items)

    def addItem(self,text:str):
        if self.count() == 0:
            self.__items.append({

            })
        elif self.count() > 0:
            pass

    def addItems(self,data:list):
        for info in data:
            pass



    def paintEvent(self, e: QPaintEvent) -> None:
        painter = QPainter(self)

        for item in self.__items:
            rect = item["bg"]["rect"] # type:QRect
            text = item["text"]["text"] # type:str
            t_pos = item["text"]["pos"] # type:QPoint

            # 绘制背景
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor("#55ffff"))
            x,y = rect.x(),rect.y()
            if rect.width() == -1:
                w = self.width()-x*2
            h = rect.height()
            painter.drawRoundedRect(x,y,w,h,5,5)

            # 绘制文本
            painter.setPen(QColor("#000"))
            f = QFont(text)
            fsize = textSize(f,text)
            fw,fh = fsize.width(),fsize.height()
            x = w//2-fw//2
            y = t_pos.y()+fh//2+5
            painter.drawText(x,y,text)

        painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = ListTree()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())