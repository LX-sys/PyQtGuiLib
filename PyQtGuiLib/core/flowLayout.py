from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QPushButton,
    QSize,
    QRect,
    QPoint,
    qt,
    QMargins,
    QLayout,
    QLayoutItem
)

'''
    流式布局
'''

class FlowLayout(QLayout):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # 边距
        self.margin = -1
        self.hSpacing = -1
        self.vSpacing = -1

        self.items = []
        self.setSpacing(6)

    def addItem(self, item: QLayoutItem) -> None:
        self.items.append(item)

    def count(self) -> int:
        return len(self.items)

    def itemAt(self, index: int) -> QLayoutItem:
        if index < self.count():
            return self.items[index]
        return None

    def takeAt(self, index: int) -> QLayoutItem:
        if (index >=0 and index < self.count()):
            return self.takeAt(index)
        return None

    def setGeometry(self, rect: QRect) -> None:
        super().setGeometry(rect)
        self.doLayout(rect,False)

    def sizeHint(self) -> QSize:
        return self.minimumSize()

    def minimumSize(self) -> QSize:
        size = QSize(0,0)
        for w in self.items:  # type:QWidget
            size = size.expandedTo(w.minimumSize())

        margins = self.contentsMargins()
        size += QSize(margins.left()+margins.right(),margins.top()+margins.bottom())
        return size

    def heightForWidth(self, width: int) -> int:
        height = self.doLayout(QRect(0,0,width,0),True)
        return height

    def doLayout(self,rect:QRect,tOnly:bool):
        left, top, right, bottom = self.getContentsMargins()
        offrect = rect.adjusted(left+1,top+1,right-1,bottom-1)
        x,y = offrect.x(),offrect.y()
        lineHeight = 0

        for w in self.items:  # type:QWidget
            wid = w.widget()
            spaceX = self.horizontalSpacing()
            if spaceX == -1:
                spaceX = wid.style().layoutSpacing(qt.PolicyPushButton,qt.PolicyPushButton,qt.Horizontal)
            spaceY = self.verticalSpacing()
            if spaceY == -1:
                spaceX = wid.style().layoutSpacing(qt.PolicyPushButton,qt.PolicyPushButton,qt.Vertical)
            nextX = x+w.sizeHint().width() + spaceX
            if (nextX - spaceX) > offrect.right() and lineHeight >0:
                x = offrect.x()
                y = y + lineHeight + spaceY
                nextX = x+w.sizeHint().width()+spaceX
                lineHeight = 0

            if not tOnly:
                w.setGeometry(QRect(QPoint(x,y),w.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight,w.sizeHint().height())
        return y+lineHeight-rect.y()+bottom

    def horizontalSpacing(self):
        if self.hSpacing >= 0:
            return self.hSpacing
        else:
            return self.smartSpacing(qt.PM_LayoutHorizontalSpacing)

    def verticalSpacing(self):
        if self.hSpacing >= 0:
            return self.hSpacing
        else:
            return self.smartSpacing(qt.PM_LayoutVerticalSpacing)

    def smartSpacing(self,pm) -> int:
        parent = self.parent()
        if not parent:
            return -1
        elif parent.isWidgetType():
            pw = QWidget()
            return pw.style().pixelMetric(pm,None,pw)
        else:
            return self.spacing()

    def removeItem(self, e: QLayoutItem) -> None:
        self.items.remove(e)

    def removeWidget(self, w: QWidget) -> None:
        for it in self.items:
            if it.widget() == w:
                self.items.remove(it)
                w.deleteLater()
                break

    # 这个方法如果返回 Flase 那么高度不在被限制
    def hasHeightForWidth(self) -> bool:
        return True

    def __del__(self):
        for w in self.items: # type:QWidget
            del w