# -*- coding:utf-8 -*-
# @time:2023/1/1320:40
# @author:LX
# @file:controlConfig.py
# @software:PyCharm

from abc import ABCMeta

class CStyleConfigABC(metaclass=ABCMeta):
    @staticmethod
    def name()->str:
        pass

    @staticmethod
    def config()->dict:
        pass


# 按钮样式
class ButtonStyleConfig(CStyleConfigABC):
    @staticmethod
    def config()->dict:
        return {
            ButtonStyleConfig.name(): [["randomStyle", "随机样式"], ["contrastStyle", "互补色样式"], ["homologyStyle", "同色调样式"]]
        }

    @staticmethod
    def name() -> str:
        return "QPushButton"


# 输入框样式
class LineEditStyleConfig(CStyleConfigABC):
    @staticmethod
    def config():
        return {LineEditStyleConfig.name():[]}

    @staticmethod
    def name() -> str:
        return "QLineEdit"

# ====================================

class StyleConfig:
    # 注册控件
    Style_Class = [
        ButtonStyleConfig,
        LineEditStyleConfig
    ]

    @staticmethod
    def getConfig():
        style_dict = dict()
        for s in StyleConfig.Style_Class:
            style_dict.update(s.config())
        return style_dict
