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
2022.12.26  0.0.6.1版本
    --- 新增轮播组件 新增两个方法,setAnimationTime(),setAinDirectionMode()
2022.12.26  0.0.7.0版本
    --- 新增线性渐变进度条,到目前为止,这是唯一个不提供文字显示的进度条
    --- 更新的所有进度条的抗锯齿写法 painter.setRenderHints(painter.Antialiasing | painter.SmoothPixmapTransform | painter.TextAntialiasing)
2023.1.4  0.0.8.0版本
    --- 线性渐变进度条 增加一个修改背景底色的方法 setBackGroundColor()
    --- 感谢[PyQt5学习爱好群-(讨厌自己)提供的BUG修复思路] 修复Borderless右下角拉伸BUG
    --- 新增 标题栏 TitleBar 类(测试发布中)
2023.1.4 0.0.8.1版本
    --- 修复 TitleBar 标题栏 在多个屏幕下的BUG
    --- TitleBar 在点击关闭按钮,新增隐退效果
    --- TitleBar 放大按钮动画增强
    --- TitleBar 增加缩小动画
2023.1.4 0.0.8.2版本
    --- TitleBar 更新Mac风格的放大,缩小,关闭按钮风格
    --- TitleBar 新增 setAniDuration() 方法 设置动画的时长
    --- TitleBar 新增 setTitleIcon(),setSyncWindowIcon() 与设置图标相关的方法
    --- 优化了TitleBar部分代码
2023.1.4 0.0.8.3版本
    --- 修复 TitleBar 类在mac下图标显示位置的问题
    --- utility.py 新增 系统判断
    --- 新增状态栏
    --- 状态栏 新增 setStatusPos() 方法
2023.1.5 0.0.8.3版本
    --- 优化 TitleBar,StatusBar 代码,并修复了样式表设置无效的BUG
2023.1.5 1.0.8.3版本
    --- 新增 styles 皮肤包项目 
    --- 全面兼容 PyQt5,PyQt6,PySide2,PySide6, PySide6 在使用无边框的还有小问题
2023.1.7 1.0.9.3版本
    --- 新增流式布局(FlowLayout)
    --- 互补色样式(contrastStyle())，同色调样式(homologyStyle())
    --- 修复 标题栏和状态栏 无法绘制文字的BUG
2023.1.8 1.0.9.4版本
    --- 修复流式布局 在mac的间距问题
    --- 优化 标题栏 和 状态栏 的代码
    --- 优化获取文字大小函数 textSize() 对丢失像素进行补偿
    --- 优化标题栏 在PyQt6,PySide6,标题高度计算不精准的Bug
2023.1.8 1.1.9.4版本
    --- 感谢! PyQt5学习爱好群-(讨厌自己)修复 PyQt6 版本下 无边框类(Borderless)移动BUG
    --- 增加 内置-样式设计器,主要是为了配合皮肤包
2023.1.9 1.1.9.5版本
    --- 标题栏和状态栏 终于 不用主窗口中重写 resizeEvent事件来调用 updateXXX() 来完成大小自适应了
    --- 修复了 内置-样式设计器 不少BUG
2023.1.9 1.2.10.5版本
    --- 新增 控件的组成分析函数 导入方式 from PyQtGuiLib.core.resolver import dumpStructure
    --- 新增 QListWidget 增强版本 - ListWidget
    --- 轮播组件重写中
2023.1.12 - 2023-1.13 [1.2.12.5] 版本
    --- 删除 文件buttonWidget.py 和 roundWidget.py
    --- 重构的 无边框的代码 增加了许多功能,请看文档
    --- 标题栏 新增了 窗口钉住功能, Win 和 Mac 各有一套风格
    --- 新增功能 滚动栏(RollWidget)
    --- ListWidget 新增一种动画效果
    --- 新增 说明 流式布局 无法 配合 QScrollArea 使用
2023.1.14 1.2.13.6
    --- 重新修改了标题栏的继承方式
    --- 更新 无边框窗口 的代码,修复无边框窗口在作为子窗口时,不显示的BUG,
        并失去做为主窗口时的部分功能
    --- 新增了一个 动态标题输入框(DynamicTLine)
    --- 对流式布局进行了优化
    --- 移除了 内置样式设计器的 controlConfig.json 改为 controlConfig.py
2023.1.15 1.2.15.6
    --- 新增开关按钮(SwitchButton)
    --- 新增调色版(ColorPalette)
2023.1.15 1.2.15.7
    --- 调色版相关问题
            1.修复中间区域无法获取颜色的BUG
            2.修复中间区域点击无法触发信号BUG
            3.新增一个获取当前选中颜色的按钮
            4.新增两个信号(colorNamed,clicked)
            5.新增两种风格(Style_Black,Style_White)
    --- 重构 气泡窗口
2023.1.20 [1.2.17.7]
    --- 气泡窗口 重构完成,并使用使用了全新的QSS来设置样式
    --- 轮播组件 重构完成
    --- 以及更新部分测试用例
'''

# ===============================================

'''
记录已知BUG,但是还未修复
轮播组件(SlideShow) 后期将重写

'''