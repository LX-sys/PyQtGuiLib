[TOC]

# python-qt组件库

### python版本需求

```
3.xxx 以上
```

### python下qt支持的版本

```
pyside2, pyside6, pyqt5, pyqt6 
```

### 系统支持

```
win
mac
```

### 项目目录说明	

```python
PyQtGuiLib
|- abandonCase   # 存放已经放弃的的案例
|- animation     # 动画功能文件
|- core          # 组件的核心实现文件
|- styles        # 基础组件皮肤包
|- header        # 公共模块,函数文件
|- Log           # 更新日志
|- tests         # 组件测试文件
```

### 其他贡献者

```python
PyQt5学习爱好群-(讨厌自己)  -- PyQtGuiLib 0.0.8.0版本
   ---> 修复了Borderless右下角拉伸BUG
PyQt5学习爱好群-(讨厌自己)  -- PyQtGuiLib 1.1.9.5版本
   ---> 修复 PyQt6 版本下 无边框类(Borderless)移动BUG
```

### 皮肤包

```python
导入方式 
from PyQtGuiLib.styles import xxx

按钮皮肤包
from PyQtGuiLib.styles import ButtonStyle

# --- Api
ButtonStyle.style()
ButtonStyle.randomStyle()  # 随机样式
ButtonStyle.contrastStyle() # 互补色样式
ButtonStyle.homologyStyle() # 同色调样式()
```

### 内置工具 - 样式设计器

```python
BuiltStyleDesigner  ---> 30%

工具位置 PyQtGuiLib -> styles -> BuiltStyleDesigner -> builtStyleDesigner.py 直接运行这个文件即可

目前支持的 控件
QPushButton  ---> 50%
```
### 解析器
```python
dumpStructure()  --> 100%
导入方式 from PyQtGuiLib.core.resolver import dumpStructure
dumpStructure(widget :QWidget ,spaceCount=0)  # 控件的组成分析函数

# ===
注意:在单独使用该函数之前,需要加 app = QApplication(sys.argv)
如果你在一个窗口类里面使用则不需要加
```
## 窗口系列
```python
导入方式 
from PyQtGuiLib.core.widgets import (
    BorderlessMainWindow, # 无边框矩形主窗口
    BorderlessFrame,      # 无边框矩形QFrame窗口
    BorderlessWidget,     # 无边框矩形QWidget窗口
    BorderlessStackedWidget  # 无边框矩形StackedWidget窗口
)

特性
无边框,可移动,可拉伸,窗口颜色风格变化多样

窗口系列 类变量
# 渐变的方向
G_Vertical
G_Horizontal

窗口系列  ---- API介绍
setRadius() # 设置圆角半径(不要超过8)
setWindowColor() # 设置窗体颜色
setWindowBorderColor() # 设置边框颜色
setEnableGColor() # 设置是否启用渐变色
setWindowGColor() # 设置窗体渐变色
setBorderStyle() # 设置变框风格
setBorderWidth() # 设置边的宽度
```
## 组件说明

### 气泡窗口(BubbleWidget)

```python
气泡窗口  ---> 100%  完成
导入方式 from PyQtGuiLib.core import BubbleWidget

气泡窗口 -- BubbleWidget API介绍

# ---类变量
Top  # 气泡方向 - 上
Down
Left
Right

# ---API
setDirection()  # 设置气泡箭头方向
setText() # 设置文字(窗口会随着文字大小而改变)
setTrack() # 控件追踪(自动出现在控件的周围)

# ----全新的QSS 设置样式例子
BubbleWidget{
qproperty-backgroundColor: rgba(165, 138, 255,200);  /*气泡背景颜色*/
qproperty-radius:10;   /*气泡圆角大小*/
qproperty-fontSize:12;  /*文字大小*/
qproperty-arrowsSize:20; /*气泡小三角的大小*/
qproperty-margin:3; /*文本框个小三角之间的距离*/
}
```

### 靠边窗口(PullOver)

```python
靠边窗口  ----> 100% 完成
导入方式 from PyQtGuiLib.core import PullOver

靠边窗口 -- PullOver API介绍
pullover() # 设置一个点击显示的按钮,窗口显示的位置,以及缩小后的位置
setEasingCurve() # 设置东西
```

### 圆环进度条(CircularBar)

```python
圆环进度条  ----> 99%
导入方式 from PyQtGuiLib.core.progressBar import CircularBar

圆环进度条 -- PullOver API介绍
# ---信号
valueChange  # 进度条变化时触发

# --- 类变量
# 变化的圈
OuterRing   # 仅外圈变化
InnerRing   # 仅内圈变化
Double      # 内外圈一起变化
# 线段的风格
SolidLine   # 直线
DashLine    # 短线
DotLine     # 点
DashDotLine # 短线和点的交替
DashDotDotLine # 短线和两个点的交替
CustomDashLine # 自定义样式(这个必须配合api使用才会生效)

# --- Api
setText()  # 设置文本
setTextColor() # 设置文本颜色
setTextSize()  # 设置文本大小
setAllText() # 同时设置文本,颜色,大小
setOuterColor() # 设置外圈颜色
setInnerColor() # 设置内圈颜色
setOuterStyle() # 设置外圈风格(线段的风格类变量)
setInnerStyle() # 设置内圈风格(线段的风格类变量)
setVariableLineSegment() # 设置变化的线段(这里的参数就前3个类变量)
setValue() # 设置进度条的值0~100
value() # 返回进度条的值
setOuterDashPattern() # 设置外圈自定义线段样式(必须配合CustomDashLine类变量才生效)
setInnerDashPattern() # 设置内圈自定义线段样式(必须配合CustomDashLine类变量才生效)
```

### 加载进度条(LoadBar)

```python
加载进度条  ----> 99%
导入方式 from PyQtGuiLib.core.progressBar import LoadBar

加载进度条 -- LoadBar API介绍

# ---信号
valueChange  # 进度条变化时触发

# --- Api
setText()  # 设置文本
setTextColor() # 设置文本颜色
setTextSize()  # 设置文本大小
setAllText() # 同时设置文本,颜色,大小
isHideText() # 设置是否需要显示进度的文字
setOuterRadius() # 设置进度条的外圆角大小(默认是20)
setInnerRadius() # 设置进度条的内圆角大小(默认是15)
setRadius() # 设置进度条的内外圆角
setBorderWidth() # 设置进度条边的宽(默认是3)
```

### 水球进度条(WaterBar)

```python
水球进度条  ----> 90%
导入方式 from PyQtGuiLib.core.progressBar import WaterBar

加载进度条 -- WaterBar API介绍

# ---信号
valueChange  # 进度条变化时触发

# --- Api
setText()  # 设置文本
setTextColor() # 设置文本颜色
setTextSize()  # 设置文本大小
setAllText() # 同时设置文本,颜色,大小
isHideText() # 设置是否需要显示进度的文字
setBallInterval() # 设置每个数值变化,球产生的个数区间(默认[1,1])
setBallSpeedInterval() # 设置每颗球移动的速度区间(默认[1200,4000])
setBallSizeInterval() # # 设置每颗球生成的大小区间(默认[5,15])
setWaterColor() # 设置水的颜色
setWaterVatColor() # 设置水缸中没有被水覆盖的颜色
setWaterVatBorderColor() # 设置水缸边缘的颜色
```

### 组件轮播(SlideShow)

```python
组件轮播  ----> 90%
导入方式 from PyQtGuiLib.core import SlideShow

组件轮播 -- WaterBar API介绍

# ---信号
changeWidget  # 切换窗口时触发

# ---- 类变量
# 动画方向模式类变量
Ani_Left
Ani_Right
Ani_Down
Ani_Up

# --- Api
addWidget()  # 添加窗口
setCurrentIndex() # 切换到指定窗口
setAutoSlideShow() # 设置自动轮播
removeWidget() # 移除窗口(仅仅只有移除轮播组件,如果需要销毁窗口,需要自己编写代码)
setAinDirectionMode() # 设置动画方向模式(例如:上下方向(SlideShow.Ani_Up,SlideShow.Ani_Down))
setButtonsHide() # 设置隐藏/显示左右按钮(默认显示)
getButtons() # 返回左右按钮对象(可以通过这个方法来重写左右按钮样式)
```

### 线性渐变进度条(GradientBar)

```python
线性渐变进度条  ----> 99%
导入方式 from PyQtGuiLib.core.progressBar import GradientBar

线性渐变进度条 -- GradientBar API介绍

# ---信号
valueChange  # 进度条变化时触发

# --- Api
setValue() # 设置当前进度0-100
setRadius() # 设置圆角半径(默认没有圆角)
setBackGroundColor() # 设置进度条底色
setColorAts() # 设置颜色比重和颜色例如 [(颜色比重0-1,QColor()),...]
appendColor() # 添加一种颜色  (颜色比重0-1,QColor())
removeColor() # 移除一种颜色 (颜色比重0-1,QColor())
getColors()  # 返回所有的颜色和比重

# -----
注意,这个进度条不提供文字显示,如果需要请自行编写
```

### 标题栏(TitleBar)

```python
标题栏  ----> 99%
导入方式 from PyQtGuiLib.core.widgets import TitleBar

标题栏 -- TitleBar API介绍

# ---- 类变量
# 标题位置
Title_Left
Title_Center
# 缩小,放大,关闭 风格
WinStyle
MacStyle

# --- Api
setTitleText()  # 设置标题
setTitleColor() # 设置标题颜色
setTitleSize()  # 设置标题字体大小
setAllTitle() # 同时设置,标题,颜色,字体大小
setTitlePos() # 设置标题的位置(例如居中: TitleBar.Title_Center)
setBtnStyle() # 设置 缩小,放大,关闭 按钮的风格(默认: TitleBar.WinStyle)
setAniDuration() # 设置动画的时长(默认300毫秒)
setTitleIcon() # 设置图标(默认会同步任务栏的图标)
setSyncWindowIcon() # 设置是否同步桌面任务栏的图标
updateTitleSize() # 更新标题栏大小

# -------
注意: 图标同步任务栏的效果只在win下才有效果
在Mac设置图标方法,下面这个设置路径是写在运行程序那里的
app = QApplication()
app.setWindowIcon(QIcon(路径))
```

### 状态栏(StatusBar)

```python
状态栏  ----> 80%  测试使用中
导入方式 from PyQtGuiLib.core.widgets import StatusBar

状态栏 -- StatusBar API介绍

# --- Api

addText() # 添加文本,可以设置持续多长时间后消失
addButton() # 添加按钮,可以设置一个点击事件
addWidget() # 添加一个窗口
addTime() # 添加时间
setTimeFormat() # 设置时间到格式(默认: %Y-%m-%d %H:%M:%S)

这里所有添加的功能都可以通过 style 参数来设置样式
```
### 流式布局(FlowLayout)
```python
流式布局  ----> 99%
导入方式 from PyQtGuiLib.core import FlowLayout

流式布局 -- FlowLayout API介绍

# --- Api
流式布局的和其他布局基本没有什么区别
addWidget()
removeWidget() 

# ----------
注意: 在使用 removeWidget() 移除控件的时候,控件会被删除掉
注意: 流式布局 无法 配合 QScrollArea 使用
```

### 滚动栏(RollWidget)

```python
滚动栏  ----> 90% 测试使用中
from PyQtGuiLib.core import RollWidget

# -- 信号
changed # 左右移动时触发信号,并返回当前子控件

# -- 动画效果
InCurve
OutBounce
CosineCurve
SineCurve

滚动栏 -- RollWidget API介绍

# --- Api
setAniEnabled() # 设置动画是否启用(默认开启)
setAniDuration() # 设置持续时间(默认200)
setAniSpecial() # 设置动画特效(参数就类变量,默认特效:InCurve)
addWidget() # 添加控件
buttons()  # 返回两个按钮对象
```

### 动态标题输入框(DynamicTLine)

```python
DynamicTLine   ----> 90% 测试使用中
导入方式 from PyQtGuiLib.core.lineedit import DynamicTLine

# --- Api
setPlaceholderText() # 设置提示文字
text() # 获取文本
label() # 返回标题对象
line()  # 返回输入框对象

```
### 开关按钮
```python
SwitchButton  --> 95% 测试使用中
导入方式 from PyQtGuiLib.core.switchButtons import SwitchButton

# --- 信号
clicked  # 点击时触发

# --- 类变量
Shape_Circle  # 圆形
Shape_Square  # 方向

# --- Api
setDefaultState()  # 设置默认状态
state()  # 返回当前的状态
setShape() # 设置形状
setBgColor() # 设置背景颜色 参数 格式 {"false":QColor,"true":QColor}
setBallColor() # 设置运行球的颜色 格式 {"false":QColor,"true":QColor}

# --------
```
### 调色版
```python
ColorPalette --> 99% 测试使用中
导入方式 from PyQtGuiLib.core import ColorPalette

# --- 类变量
Style_Black  # 黑色窗口风格
Style_White  # 白色窗口风格
Style_None   # 没有窗口风格

# --- 信号
rgbaChange  颜色改变时触发,返回的元组 (r,g,b,a)
colorNamed  颜色改变时触发,反正字符串 十六进制颜色名称
clicked     点击获取颜色按钮时触发,同时返回以上两种参数

# --- APi
setStyleMode() # 设置窗体本身的风格
getHexName()  # 当前当前十六进制颜色
getRGBA() # 返回当前RGBA颜色
```
## 控件增强
### QListWidget 增强 - ListWidget

```python
ListWidget ---> 99% 
导入方式 from PyQtGuiLib.core import ListWidget

# 类变量 - 添加/移除窗口时的动画特效
OutBounce
CosineCurve
SineCurve

# ----- Api
setAniEnabled() # 设置动画是否启用(默认开启)
setAniDuration() # 设置持续时间(默认300)
setAniSpecial() # 设置动画特效(参数就类变量,默认特效:OutBounce)
setItemMinHeight() # 设置item的最小高度(默认:30)
addWidget() # 添加 QWidget
removeWidget() # 移除窗口
getAllWidget() # 返回所有窗口
```

