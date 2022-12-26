# -*- coding:utf-8 -*-
# @time:2022/12/128:53
# @author:LX
# @file:developmentLog.py
# @software:PyCharm
'''
    开发日志文件
'''


'''
2022.12.13  0.0.1.4版本  气泡窗口已经基本实现,持续优化更新
2022.12.13  0.0.1.5版本  重写了气泡窗口的部分实现代码
2022.12.19  0.0.2.0版本
    --- 气泡窗口 优化了代码,修复了文字大小无法设置的BUG,以及文字位置的问题
    --- 新增无边框窗口 BorderlessWidget 类,导入方式 from PyQtGuiLib.core.widgets import BorderlessWidget
    --- 新增圆角窗口 RoundWidget 类,导入方式 from PyQtGuiLib.core.widgets import RoundWidget
    --- 靠边窗口功能完成(任意窗口都可以加上该功能),PullOver类 导入方式 from PyQtGuiLib.core.pullOver import PullOver
    --- 靠边窗口功能的测试用例已编写
2022.12.20  0.0.3.0版本
    --- 新增圆环进度条
2022.12.22  0.0.4.0版本
    --- 修复了一些小的BUG
    --- 放弃了亚克力窗口的研究
    --- 新增加载进度条
2022.12.22  0.0.5.0版本
    --- 新增水球进度条
    --- 新增进度条的集合测试
    --- 修改了气泡窗口的导入方式
         原来的导入方式: from PyQtGuiLib.core.bubbleWidget import BubbleWidget
         现在的导入方式: from PyQtGuiLib.core import BubbleWidget
    --- 修改了窗口靠边功能的导入方式
         原来的导入方式: from PyQtGuiLib.core.pullOver import PullOver
         现在的导入方式: from PyQtGuiLib.core import PullOver
2022.12.26  0.0.6.0版本
    --- 新增轮播组件,2022.12.22  已经基本完成,可能还存在BUG,以后修改(测试发布)
'''