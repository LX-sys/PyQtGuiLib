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

### 安装方式

```
pip install PyQtGuiLib
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
![](https://github.com/LX-sys/PyQtGuiLib/blob/master/gif/%E5%86%85%E7%BD%AE%E6%A0%B7%E5%BC%8F%E8%AE%BE%E8%AE%A1%E5%99%A8.gif)
### 解析器
```python
dumpStructure()  --> 100%
导入方式 from PyQtGuiLib.core.resolver import dumpStructure
dumpStructure(widget :QWidget ,spaceCount=0)  # 控件的组成分析函数

# ===
注意:在单独使用该函数之前,需要加 app = QApplication(sys.argv)
如果你在一个窗口类里面使用则不需要加
```
![](https://github.com/LX-sys/PyQtGuiLib/blob/master/gif/%E6%8E%A7%E4%BB%B6%E7%9A%84%E7%BB%84%E6%88%90%E5%88%86%E6%9E%90.gif)
### QSS 样式解析器(QssStyleAnalysis)

```python
QssStyleAnalysis  ---> 99%(测试中) 

导入方式 from PyQtGuiLib.styles import QssStyleAnalysis

Api ------
setParent() # 设置父类对象
setQSS(样式字符串) # 设置样式
setQSSDict(字典样式) # 设置样式
appendQSS(样式字符串) # 追加样式
appendQSSDict(字典样式) # 追加样式

toStr() # 返回样式的原始字符串
toDict() # 返回样式的字典
selector(选择器or下标) # 返回QSS对象
   --- header() # 返回选择器的名称
   --- headerSubdivision() # 返回列表形式的选择器名称
   --- body() # 返回属性的原始字符串类型
   --- bodySubdivision() # 将原始属性以列表的形式返回
   --- bodyToDict() # 将原始属性以字典的形式返回(不带选择器)
   --- toDict() # 将原始属性以字典的形式返回(带选择器)
   --- attr(key) # 返回属性的值
   --- updateAttr(key,value) # 更新/增加一个属性的值
   --- removeAttr(key) # 移除一个属性
removeSelector(选择器or下标) # 移除该选择器的样式
inherit() # 样式传承 (详细用法查看 eg3案例) 

# ============
代码案例位置
PyQtGuiLib -> tests -> test_QssStyleAnalysis 目录下
```



## 窗口系列

```python
导入方式
from PyQtGuiLib.abandonCase.widgets import (
    BorderlessWidget,  # 无边框QWidget窗口
)

特性
无边框, 可移动, 可拉伸, 窗口颜色风格变化多样

窗口系列 - --- API介绍
setEnableGColor()  # 设置是否启用渐变色

自定义QSS  --- 目前支持的
qproperty-radius  --> 圆角  Eg: 7
qproperty-backgroundColor  --> 背景颜色 Eg: rgba(165, 138, 255,200)
qproperty-borderWidth --> 边的宽度 Eg: 1
qproperty-borderStyle --> 边框的风格 Eg: solid
qproperty-borderColor --> 边框颜色 Eg: rgba(0,100,255,255)
qproperty-border   --> 边框样式 Eg: "3 solid rgba(0,100,255,255)"
qproperty-linearDirection; --> 线性渐变的方向 Eg: "LR"
    LR: 左->右
    RL: 右->左
    UD: 上->下
    DU: 下->上
    LRANG: 左上角->右下角
    RLANG: 右下角->左上角
    UDANG: 右上角->左下角
    DUANG: 左下角->右上角
    自定义: [0,0,100,100]或者[0,0,w,h]  这里的 w,h 代只窗口当前的宽和高
qproperty-linearColor --> 线性渐变色 Eg: "rgba(142, 144, 69, 255) rgba(176, 184, 130, 255) rgba(255, 255, 255, 255)"
qproperty-linear --> 线性渐变
    Eg: "LR rgba(142, 144, 69, 255) rgba(176, 184, 130, 255) rgba(130, 184, 130, 255)";
    Eg: "[0,0,w,h] rgba(142, 144, 69, 255) rgba(176, 184, 130, 255) rgba(130, 184, 130, 255)";


```
![](https://github.com/LX-sys/PyQtGuiLib/blob/master/gif/%E6%97%A0%E8%BE%B9%E6%A1%86%E7%AA%97%E5%8F%A3.gif)
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
![](https://github.com/LX-sys/PyQtGuiLib/blob/master/gif/%E6%B0%94%E6%B3%A1%E7%AA%97%E5%8F%A3.gif)

### 靠边窗口(PullOver)

```python
靠边窗口  ----> 100% 完成
导入方式 from PyQtGuiLib.core import PullOver

靠边窗口 -- PullOver API介绍
pullover() # 设置一个点击显示的按钮,窗口显示的位置,以及缩小后的位置
setEasingCurve() # 设置东西
```
![](https://github.com/LX-sys/PyQtGuiLib/blob/master/gif/%E7%AA%97%E5%8F%A3%E9%9D%A0%E8%BE%B9.gif)
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
setOuterStyle() # 设置外圈风格(线段的风格类变量)
setInnerStyle() # 设置内圈风格(线段的风格类变量)
setVariableLineSegment() # 设置变化的线段(这里的参数就前3个类变量)
setValue() # 设置进度条的值0~100
value() # 返回进度条的值
setOuterDashPattern() # 设置外圈自定义线段样式(必须配合CustomDashLine类变量才生效)
setInnerDashPattern() # 设置内圈自定义线段样式(必须配合CustomDashLine类变量才生效)

自定义QSS
CircularBar{
qproperty-color:rgba(100,100,100,255);
qproperty-fontSize:15;
qproperty-outerColor:rgba(100,255,100,255);
qproperty-innerColor:rgba(100,255,100,255);
}
```
![](https://github.com/LX-sys/PyQtGuiLib/blob/master/gif/%E7%8E%AF%E5%BD%A2%E8%BF%9B%E5%BA%A6%E6%9D%A1.gif)
### 加载进度条(LoadBar)

```python
加载进度条  ----> 99%
导入方式 from PyQtGuiLib.core.progressBar import LoadBar

加载进度条 -- LoadBar API介绍

# ---信号
valueChange  # 进度条变化时触发

# --- Api
setText()  # 设置文本
isHideText() # 设置是否需要显示进度的文字

自定义QSS
LoadBar{
qproperty-color:rgba(100,200,100,255);
qproperty-fontSize:10;
qproperty-outerRadius:20;
qproperty-innerRadius:15;
}
```
![](https://github.com/LX-sys/PyQtGuiLib/blob/master/gif/%E5%8A%A0%E8%BD%BD%E8%BF%9B%E5%BA%A6%E6%9D%A1.gif)
### 水球进度条(WaterBar)

```python
水球进度条  ----> 90%
导入方式 from PyQtGuiLib.core.progressBar import WaterBar

水球进度条 -- WaterBar API介绍

# ---信号
valueChange  # 进度条变化时触发

# --- Api
setText()  # 设置文本
isHideText() # 设置是否需要显示进度的文字
setBallInterval() # 设置每个数值变化,球产生的个数区间(默认[1,1])
setBallSpeedInterval() # 设置每颗球移动的速度区间(默认[1200,4000])
setBallSizeInterval() # # 设置每颗球生成的大小区间(默认[5,15])

自定义QSS
WaterBar{
qproperty-color:rgba(100,200,100,255);
qproperty-fontSize:20;
/*qproperty-waterColor:rgba(0,255,0,255);
qproperty-waterVatBorderColor:rgba(0,173,0,255);
qproperty-waterVatColor:rgba(0,170,255,255);*/
}
```
![](https://github.com/LX-sys/PyQtGuiLib/blob/master/gif/%E6%B0%B4%E7%90%83%E8%BF%9B%E5%BA%A6%E6%9D%A1.gif)
### 轮播组件(SlideShow)

```python
轮播组件  ----> 90%
导入方式 from PyQtGuiLib.core import SlideShow

轮播组件 -- WaterBar API介绍

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
![](https://github.com/LX-sys/PyQtGuiLib/blob/master/gif/%E8%BD%AE%E6%92%AD%E7%BB%84%E4%BB%B6.gif)
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
![](https://github.com/LX-sys/PyQtGuiLib/blob/master/gif/%E7%BA%BF%E6%80%A7%E6%B8%90%E5%8F%98%E8%BF%9B%E5%BA%A6%E6%9D%A1.gif)
### 标题栏(TitleBar重写中)

```python
标题栏 - ---> 99 % 
导入方式
from PyQtGuiLib.abandonCase.widgets import TitleBar

标题栏 - - TitleBar
API介绍

# ---- 类变量
# 标题位置
Title_Left
Title_Center
# 缩小,放大,关闭 风格
WinStyle
MacStyle

# --- Api
setTitleText()  # 设置标题
setTitleColor()  # 设置标题颜色
setTitleSize()  # 设置标题字体大小
setAllTitle()  # 同时设置,标题,颜色,字体大小
setTitlePos()  # 设置标题的位置(例如居中: TitleBar.Title_Center)
setBtnStyle()  # 设置 缩小,放大,关闭 按钮的风格(默认: TitleBar.WinStyle)
setAniDuration()  # 设置动画的时长(默认300毫秒)
setTitleIcon()  # 设置图标(默认会同步任务栏的图标)
setSyncWindowIcon()  # 设置是否同步桌面任务栏的图标
updateTitleSize()  # 更新标题栏大小

# -------
注意: 图标同步任务栏的效果只在win下才有效果
在Mac设置图标方法, 下面这个设置路径是写在运行程序那里的
app = QApplication()
app.setWindowIcon(QIcon(路径))
```

### 状态栏(StatusBar重写中)

```python
状态栏 - ---> 80 % 测试使用中
导入方式
from PyQtGuiLib.abandonCase.widgets import StatusBar

状态栏 - - StatusBar
API介绍

# --- Api

addText()  # 添加文本,可以设置持续多长时间后消失
addButton()  # 添加按钮,可以设置一个点击事件
addWidget()  # 添加一个窗口
addTime()  # 添加时间
setTimeFormat()  # 设置时间到格式(默认: %Y-%m-%d %H:%M:%S)

这里所有添加的功能都可以通过
style
参数来设置样式
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
![](https://github.com/LX-sys/PyQtGuiLib/blob/master/gif/%E6%B5%81%E5%BC%8F%E5%B8%83%E5%B1%80.gif)
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
![](https://github.com/LX-sys/PyQtGuiLib/blob/master/gif/%E6%BB%9A%E5%8A%A8%E6%A0%8F.gif)
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
![](https://github.com/LX-sys/PyQtGuiLib/blob/master/gif/%E5%8A%A8%E6%80%81%E6%A0%87%E9%A2%98%E8%BE%93%E5%85%A5%E6%A1%86.gif)
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
![](https://github.com/LX-sys/PyQtGuiLib/blob/master/gif/%E5%BC%80%E5%85%B3%E6%8C%89%E9%92%AE.gif)
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
![](https://github.com/LX-sys/PyQtGuiLib/blob/master/gif/%E8%B0%83%E8%89%B2%E6%9D%BF.gif)
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
![](https://github.com/LX-sys/PyQtGuiLib/blob/master/gif/QListWidget%E5%A2%9E%E5%BC%BA%E7%89%88%E6%9C%AC.gif)
