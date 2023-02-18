# -*- coding:utf-8 -*-
# @time:2023/2/189:55
# @author:LX
# @file:styleLinker.py
# @software:PyCharm

'''
    样式链接器(属于外置工具)
    解决在程序运行过中,去动态的调节样式

'''
import re
import uuid
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QPushButton,
    QLabel,
    QTabWidget,
    QObject,
    qt,
    QGroupBox
)
from PyQtGuiLib.styles import QssStyleAnalysis
from PyQtGuiLib.core import PaletteFrame


class StyleLinker(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("动态样式链接器")
        self.setWindowFlag(qt.WindowStaysOnTopHint,True)
        self.resize(300,300)
        # 控件对象列表
        self.__objs = []
        # qss解析对象列表
        self.__qssAny = [] # type:[QssStyleAnalysis]

        # 全局共享 操作对象
        self.global_var = None  # type: QssStyleAnalysis

        self.defaultPage = QWidget()
        self.addTab(self.defaultPage,"样式代码")
        self.tabBarClicked.connect(self.changeTab_Event)

    # 切换操作对象
    def changeTab_Event(self,index):
        if index:
            self.global_var = self.__qssAny[index-1]

    def addQObject(self,obj:QObject):
        self.__objs.append(obj)

    def addQObjects(self,objs):
        self.__objs.extend(objs)

    def createTab(self,name):
        wid = QWidget()
        # --- 加载组件
        self.updateColorModule(wid)
        # ---- 加载组件
        self.addTab(wid,name)

    def show(self) -> None:
        for obj in self.__objs:
            qssaAng = QssStyleAnalysis(obj)
            bool_style = bool(obj.styleSheet())
            q = re.findall("QtWidgets\.(.*)\'", str(type(obj)))[0]
            qss = '''
%s{

}
                        ''' % q
            if bool_style:
                qssaAng.setQSS(obj.styleSheet())
                qssaAng.appendQSS(qss)
            else:
                qssaAng.setQSS(qss)
            self.__qssAny.append(qssaAng)
            # ------------------------------------
            if hasattr(obj,"text"):
                if obj.text():
                    self.createTab(obj.text())
                    continue
            if obj.objectName():
                self.createTab(obj.objectName())
                continue
            try:
                name = re.findall("(0x.*)>",str(obj))[0]
            except:
                name = uuid.uuid4()
            self.createTab(name)
        # 设置默认操作tab为 0
        if self.__objs:
            self.global_var = self.__qssAny[0]
            print(self.global_var)
        super().show()

    # -----
    # 更新颜色的组件 (需要重构)
    def updateColorModule(self,widget):
        def open_PaletteFrame():

            def updateBG(rgba):
                head = self.global_var.header()[0]
                self.global_var.selector(head).updateAttr("background-color",
                                                          "rgba(%s, %s, %s,%s)"%rgba)
            p = PaletteFrame() # 创建颜色版
            p.rgbaChange.connect(updateBG)
            # for head in headers:
            #     self.global_var.selector(head)
            p.show()

        group_box = QGroupBox("调色区域",widget)
        group_box.resize(200,120)
        bgbtn = QPushButton("背景颜色",group_box)
        bgbtn.move(10,20)
        bgbtn.clicked.connect(open_PaletteFrame)


class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800,600)

        self.btn = QPushButton("测试1",self)
        self.btn.setStyleSheet('''
        QPushButton{
        background-color: rgb(255, 85, 127);
        }
        ''')
        self.l2 = QLabel("我是标签",self)
        self.btn.move(10,10)
        self.l2.move(40,40)

        self.styleLinker = StyleLinker()
        self.styleLinker.addQObjects([self.btn,self.l2])
        self.styleLinker.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())