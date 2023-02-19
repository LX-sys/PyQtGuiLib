# -*- coding:utf-8 -*-
# @time:2023/2/1810:31
# @author:LX
# @file:controlType.py
# @software:PyCharm

__all__ = ["getStyleLists","getStyleCommentLists"]

STYLE_LIB = {
    ("QPushButton",):{"QPushButton":"/*按钮*/",
                       "QPushButton:hover":"/*鼠标放在按钮上时的样式*/",
                       "QPushButton:pressed":"/*按钮按下时的样式*/",
                       "QPushButton::menu-indicator":"/*菜单指示器子控件(在菜单栏时的样式)*/",
                       "QPushButton:open":"/*按钮在菜单打开时的样式*/"},
    ("QLabel",): {"QLabel": "/*标签*/",
                  "QLabel:hover": "/*鼠标放在标签上时的样式*/"
               }
}


def getStyles(key):
    if isinstance(key,str):
        key = key,
    return STYLE_LIB[key]


# 返回可操作的样式列表
def getStyleLists(key)->list:
    return list(getStyles(key).keys())


# 返回可操作的样式列表说明
def getStyleCommentLists(key)->list:
    return list(getStyles(key).values())


# 融合两个样式列表
def getMergeStyles(style1:list,style2:list)->list:
    return list(set(style1) | set(style2))


print(getMergeStyles(["QPushButton"],["QPushButton","QPushButton:hover"]))
