# -*- coding:utf-8 -*-
# @time:2023/4/179:03
# @author:LX
# @file:toolNewProject.py
# @software:PyCharm
import os,sys
from datetime import datetime as dt


def cuTime() -> str:
    return dt.strftime(dt.now(), "%Y-%m-%d %H:%M")

# 普通控件模板
TemplateCode = r'''# -*- coding:utf-8 -*-
# @time:{cutime}
# @author:LX
# @file:{title_className}.py
# @software:PyCharm

from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
)

{explain}

class {className}(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = {className}()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
'''
# 绘图控件模板
PainterTemplateCode = r'''# -*- coding:utf-8 -*-
# @time:{cutime}
# @author:LX
# @file:{title_className}.py
# @software:PyCharm

from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QPoint,
    QPainter,
    QColor,
    QRect,
    QSize,
    QFont,
    QPen,
    QBrush,
    QPaintEvent,
    Qt,
    qt
)

{explain}

class {className}(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)
    
    def paintEvent(self, e:QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)
        
        painter.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = {className}()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
'''

# -----------------------------------------------------------
# 根据个人情况经行配置
# 项目路径,测试项目路径
Project_Path = r"D:\code\PyQtGuiLib\PyQtGuiLib\core"
Test_Project_Path = r"D:\code\PyQtGuiLib\tests"


print("----------------------创建项目--------------------------")
project_name = input("输入项目名称:")
print("[1]创建普通控件 [2]绘图控件")
con_op = input("请选择:")
if con_op == '2':
    TemplateCode = PainterTemplateCode

print("[1]创建单个文件 [2]创建包")
createDir = input("请选择:")
if createDir == '1':
    create_file_path = os.path.join(Project_Path, project_name + ".py")
elif createDir == '2':
    file_name = input("请输入包名称:")
    create_page_dir = os.path.join(Project_Path, file_name)
    create_file_path = os.path.join(create_page_dir, file_name + ".py")
    print(create_file_path)

print("------------开始创建测试文件---------")
print("[1]创建单个测试文件 [2]创建包")
test_file = input("请选择:")
if test_file == '1':
    test_create_file_path = os.path.join(Test_Project_Path,"test_{}.py".format(project_name))
elif test_file == '2':
    test_create_page_dir = os.path.join(Test_Project_Path, "test_"+project_name)
    test_create_file_path = os.path.join(test_create_page_dir, "test_{}.py".format(project_name))

    print(test_create_page_dir)


print(create_file_path)

print(test_create_file_path)

# --------------------开始创建文件------------------------

if createDir == '1':
    if os.path.isfile(create_file_path):
        raise Exception("{} 已存在".format(create_file_path))
    else:
        with open(create_file_path,"w",encoding="utf8") as f:
            f.write(TemplateCode.format(cutime=cuTime(),title_className=project_name,className=project_name.title(),explain=""))
elif createDir == '2':
    if os.path.isdir(create_page_dir):
        raise Exception("{} 已存在".format(create_page_dir))
    else:
        os.mkdir(create_page_dir)
        open(os.path.join(create_page_dir,"__init__.py"),"w",encoding="utf8")
        with open(create_file_path,"w",encoding="utf8") as f:
            f.write(TemplateCode.format(cutime=cuTime(),title_className=project_name,className=project_name.title(),explain=""))

if test_file == '1':
    if os.path.isfile(test_create_file_path):
        raise Exception("{} 已存在".format(test_create_file_path))
    else:
        with open(test_create_file_path, "w",encoding="utf8") as f:
            f.write(TemplateCode.format(cutime=cuTime(),title_className=project_name,className="Test_"+project_name.title(), explain="# 测试文件"))
elif test_file == '2':
    if os.path.isdir(test_create_page_dir):
        raise Exception("{} 已存在".format(test_create_page_dir))
    else:
        os.mkdir(test_create_page_dir)
        open(os.path.join(test_create_page_dir,"__init__.py"),"w",encoding="utf8")
        with open(test_create_file_path, "w",encoding="utf8") as f:
            f.write(TemplateCode.format(cutime=cuTime(),title_className=project_name,className="Test_"+project_name.title(), explain="# 测试文件"))

