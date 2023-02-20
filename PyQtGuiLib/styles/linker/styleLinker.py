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
    QObject,
    qt,
    QGroupBox,
    QTreeWidgetItem
)
from PyQtGuiLib.styles import QssStyleAnalysis
from PyQtGuiLib.core import PaletteFrame,FlowLayout

from PyQtGuiLib.styles.linker.styleLinkerUi import StyleLinkerUI
from PyQtGuiLib.styles.linker.controlType import getStyleLists,getStyleCommentLists,getMergeStyles
from PyQtGuiLib.styles.linker.component import (
    colorComponent,
    geometryComponent,
    borderComponent,
    RegisterComponent
)
'''
    动态样式链接器
'''


class StyleLinker(StyleLinkerUI):
    def __init__(self):
        super().__init__()

        # 控件对象列表, qss解析对象列表,全局共享QSS解析器操作对象,全局共享选择器(在切换tab时切换)
        '''
            self.global_var 在切换根节点的同时,设置 QSS解析器对象
            self.global_select 在切换Tab的同时,切换当前 QSS解析器对象 的 选择器对象
        '''
        self.__objs = []
        self.__qssAny = []  # type:[QssStyleAnalysis]
        self.global_var = None  # type: QssStyleAnalysis
        self.global_select = None # type:str

        # 记录根节点对象,同时记录QSS解析器对象,方便后期判断
        # [{"root":Xxx,"qss":xxx}]
        self.record_tree_root = []
        self.buffer_tree_root = [] # 缓冲区

        self.myEvent()

    def addQObject(self,obj:QObject):
        '''
            在添加控件对象的同时,创建该对象QSS解析器对象
            如果该控件有样式,则继承,如果没有则创建出一个默认的空样式,
            还会创建一个对应的树节点(父节点+子节点),
                        --- 后期,根据点击树节点,创建一系列tab节点
        '''
        if obj in self.__objs:  # 如果出现重复对象,直接忽略
            return

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

        # 获取名称
        if hasattr(obj, "text"):
            if obj.text():
                name = obj.text()
        elif obj.objectName():
            name = obj.objectName()
        else:
            try:
                name = re.findall("(0x.*)>", str(obj))[0]
            except:
                name = uuid.uuid4()

        # 创建树根节点,以及子节点
        treeRoot = QTreeWidgetItem(self.tree())
        treeRoot.setText(0,name)
        self.record_tree_root.append({"root":treeRoot,"qss":qssaAng})

        '''
            对样式进行融合,如果该样式没有在QSS解析器中,则添加,
            最后在创建出子节点,再创建子节点的同时补上样式说明
        '''
        child_notes = getMergeStyles(qssaAng.header(),getStyleLists(q))
        for select in child_notes:
            if qssaAng.isSelectKey(select) is False:
                qssaAng.appendQSSDict({
                    select:{}
                })
        # 获取样式的说明
        comments = getStyleCommentLists(q)
        child_notes_zip = zip(child_notes,comments)
        for select,comment in child_notes_zip:
            child_tree = QTreeWidgetItem(treeRoot)
            child_tree.setText(0,select)
            child_tree.setToolTip(0,comment)

        self.__qssAny.append(qssaAng)
        self.__objs.append(obj)

    def addQObjects(self,objs):
        for obj in objs:
            self.addQObject(obj)

    # ----------------------

    def changeTab_Event(self,index):
        '''
            在切换 Tab 的同时根据tab的名称,区切换,当前QSS解析器对象的选择器名称
        '''
        if index:
            tab_name = self.tab().tabText(index)
            self.global_select = tab_name

    def doubleClickTree_Event(self,item:QTreeWidgetItem):
        '''
            双击树,获取根节点,同时设置为全局共享的操作对象,每当获取一个根节点,
            就将这个根节点加入缓冲区,方便下次查找,
            在通过根节点,找到下面的子节点,并创建出tab,
            在切换根节点时,先清空tab再创建,

            如果点击的是子节点,
                如果table存在,则切换换到对应table,如果不存在,则什么都不做
                这一段是存在BUG的(2023.2.20)
        '''

        # 判断是否点击的子节点
        child_flag = True
        for d in self.record_tree_root:
            if item == d["root"]:
                child_flag = False
                break

        if child_flag:
            child_name = item.text(0)
            table_count = self.tab().count()
            for i in range(table_count):
                if self.tab().tabText(i) == child_name:
                    self.tab().setCurrentIndex(i)
                    self.global_select = child_name # 重新设置选择器
                    break
            return
        # ------

        tab_count = self.tab().count()
        if tab_count > 1:
            for i in range(tab_count, 0, -1):
                self.tab().removeTab(i)

        root = None  # type:QTreeWidgetItem

        if item in self.buffer_tree_root: # 在缓冲区里面查找
            root = item
            for d in self.buffer_tree_root:
                if d["root"] == item:
                    self.global_var = d["qss"]
                    self.showStyleBrowserCode(self.global_var.toStr())
                    break

        if root is None:
            for d in self.record_tree_root:
                if d["root"] == item:
                    root = item
                    self.global_var = d["qss"]
                    self.buffer_tree_root.append(d)
                    self.showStyleBrowserCode(self.global_var.toStr())
                    break

        if root:
            for c in range(root.childCount()):
                child = root.child(c)
                tab_name = child.text(0)
                self.createTab(tab_name)

    # 通过树的根节点来查找 QSS解析器对象
    def getObj(self,root:QTreeWidgetItem) -> QssStyleAnalysis:
        for d in self.record_tree_root:
            if d["root"] == root:
                return d["qss"]

    def showStyleBrowserCode(self,style):
        self.browser().clear()
        self.browser().append(style)

    # 注册组件
    def registerComponent(self,flow):
        # 通用的颜色组件
        # colorComponent(self,wid)
        # geometryComponent(self,wid)
        # borderComponent(self,wid)
        for regF in RegisterComponent.getRegister():
            regF(self,flow)

    # 创建tab
    def createTab(self, name):
        wid = QWidget()
        flow = FlowLayout(wid) # 加入流式布局
        # ----
        ''''
            在wid上面添加各种组件
        '''
        # self.test_ColorModule(wid)
        self.registerComponent(flow)
        # ----
        self.tab().addTab(wid,name)

    # 颜色组件,这个函数用于测试
    def test_ColorModule(self,widget):
        def open_PaletteFrame():
            def updateBG(rgba):
                if self.global_select is None:
                    head = self.global_var.header()[0]
                else:
                    head = self.global_select
                self.global_var.selector(head).updateAttr("background-color",
                                                          "rgba(%s, %s, %s,%s)"%rgba)
            p = PaletteFrame() # 创建颜色版
            p.rgbaChange.connect(updateBG)

            p.show()

        group_box = QGroupBox("调色区域", widget)
        group_box.resize(200, 120)
        bgbtn = QPushButton("背景颜色", group_box)
        bgbtn.move(10, 20)
        bgbtn.clicked.connect(open_PaletteFrame)

    def myEvent(self):
        self.tab().tabBarClicked.connect(self.changeTab_Event)
        self.tree().itemDoubleClicked.connect(self.doubleClickTree_Event)

# =====================================
# 下面是测试用例

class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800,600)

        self.btn = QPushButton("测试1",self)
        self.btn.setStyleSheet('''
        QPushButton{
        background-color: rgb(255, 85, 127);
        }
        QPushButton:hover{
        background-color: rgb(0, 85, 127);
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