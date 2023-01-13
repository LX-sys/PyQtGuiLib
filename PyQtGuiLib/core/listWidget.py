from PyQtGuiLib.header import (
    QListWidget,
    QListWidgetItem,
    QWidget,
    QSize,
    QPropertyAnimation,
    QPoint,
    qt
)

'''
    QListWidget 增强版本 - ListWidget
'''

class ListWidgetItem(QListWidgetItem):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)


class ListWidget(QListWidget):
    InCurve = qt.InCurve
    OutBounce = qt.OutBounce
    CosineCurve = qt.CosineCurve
    SineCurve = qt.SineCurve


    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        # 存储(item,widget)
        self.widgets = []

        # item的最小高度
        self.item_min_height = 30

        # 动画是否启用,持续时间,动画特效
        self.ani_enabled = True
        self.ani_duration = 300
        self.ani_special = ListWidget.OutBounce

        self.defaultStyle()

    # 设置动画是否启用
    def setAniEnabled(self,b:bool):
        self.ani_enabled = b

    # 设置持续时间
    def setAniDuration(self, duration:int):
        self.ani_duration = duration

    # 设置动画特效
    def setAniSpecial(self,special):
        self.ani_special = special

    # 设置item的最小高度
    def setItemMinHeight(self,h:int):
        self.item_min_height = h

    # 添加 QWidget
    def addWidget(self,widget:QWidget):
        widget.setFixedHeight(self.item_min_height)

        item = ListWidgetItem()
        item.setSizeHint(QSize(self.width()-4,widget.height()))
        self.widgets.append((item, widget))

        def _t(self,item,widget):
            self.addItem(item)
            self.setItemWidget(item, widget)
            if self.ani_enabled:
                temp_ani_widget.deleteLater()

        if self.ani_enabled:
            # ----------动画
            # 先创建临时动画窗口
            temp_ani_widget = QWidget(self)
            temp_ani_widget.resize(item.sizeHint())
            temp_ani_widget.setStyleSheet(widget.styleSheet())
            temp_ani_widget.move(0,self.height()-temp_ani_widget.height()-1)
            temp_ani_widget.show()

            ani = QPropertyAnimation(temp_ani_widget)
            ani.setTargetObject(temp_ani_widget)
            ani.setPropertyName(b"pos")
            ani.setStartValue(temp_ani_widget.pos())
            ani.setEndValue(QPoint(0,(len(self.widgets)-1)*self.item_min_height))
            ani.setDuration(300)
            ani.setEasingCurve(self.ani_special)
            ani.start()

            ani.finished.connect(lambda :_t(self,item,widget))
        else:
            _t(self,item,widget)
        # ----------动画

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

                def _t(self,item,wid,i):
                    self.removeItemWidget(item)
                    wid.deleteLater()
                    self.takeItem(i)
                    del item

                if self.ani_enabled:
                    # -------------
                    # 移除动画
                    ani = QPropertyAnimation(wid)
                    ani.setTargetObject(wid)
                    ani.setPropertyName(b"pos")
                    ani.setStartValue(wid.pos())
                    ani.setEndValue(QPoint(0, self.height()-self.item_min_height))
                    ani.setDuration(300)
                    ani.setEasingCurve(self.ani_special)
                    ani.start()

                    ani.finished.connect(lambda :_t(self,item,wid,i))
                    # -------------
                else:
                    _t(self, item, wid, i)
                break