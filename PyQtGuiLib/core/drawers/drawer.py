# -*- coding:utf-8 -*-
# @time:2023/4/2013:48
# @author:LX
# @file:drawer.py
# @software:PyCharm

from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QScrollArea,
    Qt
)

from PyQtGuiLib.animation import Animation


class DrawerItem(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(300, 300)

        self.__vboy = QVBoxLayout(self)
        self.__vboy.setSpacing(0)
        self.__vboy.setContentsMargins(0,0,0,0)

        self.btn = QPushButton("点击")
        self.btn.setMinimumHeight(50)
        self.btn.clicked.connect(self.stretch_event)

        self.expansion_widget = QWidget()
        self.expansion_widget.setStyleSheet('''
        background-color: rgb(85, 170, 127);
        ''')

        self.setFixedHeight(50)

        self._sp = QSpacerItem(0,0,QSizePolicy.Minimum,QSizePolicy.Expanding)

        self.__vboy.addWidget(self.btn)
        self.__vboy.addWidget(self.expansion_widget)
        self.__vboy.addItem(self._sp)

        self.__flag = False

    def stretch_event(self):
        self.__ani = Animation()
        self.__ani.setStartMode(Animation.Parallel)
        if self.__flag is False:
            self.__ani.addAni(self.btn.height(),300,duration=200,courseFunc=self.setFixedHeight)
            self.__ani.addAni(self.expansion_widget.height(),300,duration=200,courseFunc=self.expansion_widget.setFixedHeight)
            self.__flag = True
        else:
            self.__ani.addAni(self.height(),self.btn.height(),duration=200,courseFunc=self.setFixedHeight)
            self.__ani.addAni(self.expansion_widget.height(), 0,duration=200, courseFunc=self.expansion_widget.setFixedHeight)
            self.__flag = False
        self.__ani.start()


class Drawer(QScrollArea):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

        self.setWidgetResizable(True)

        self.__core = QWidget()

        self.setWidget(self.__core)

        self._vboy = QVBoxLayout(self.__core)
        self._vboy.setSpacing(0)
        self._vboy.setContentsMargins(0,0,0,0)
        self._sp = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)


        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for _ in range(4):
            self.addItem(DrawerItem())

    def addItem(self,item:DrawerItem):
        self._vboy.removeItem(self._sp)
        self._vboy.addWidget(item)
        self._vboy.addItem(self._sp)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Drawer()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())