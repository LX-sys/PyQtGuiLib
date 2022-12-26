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
|- header        # 公共模块,函数文件
|- Log           # 更新日志
|- tests         # 组件测试文件
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

Be_Forever # 如果将气泡的持续时间这个为这个,气泡将永远不会消失
# ---API
setAnimationEnabled() # 是否启用气泡启动动画
setDurationTime() # 气泡持续时间
setTrack() # 追踪控件(气泡会一直依附在控件周围)
setText()  # 设置文本
setTextColor() # 设置文本颜色
setTextSize()  # 设置文本大小
setAllText() # 同时设置文本,大小,颜色
setKmPos() # 设置三角形的位置
setKmDiameter() # 设置三角形的垂直高度
setKmM() # 设置三角形的开口大小
setKm() # 同时设置三角形的位置,垂直高度,开口大小
setDirection() # 设置气泡的方向
setBColor() # 设置背景颜色

# 注意在气泡动画和持续时间同时开启时
设置持续时间的代码一定要在,设置启动动画的前面
# 注意在设置方向和追踪时
设置方向的代码一定要在追踪前面
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

### 轮播组件(SlideShow)

```python
轮播组件  ----> 90%
导入方式 from PyQtGuiLib.core import SlideShow

轮播组件 -- WaterBar API介绍

# ---信号
switchWidgeted  # 切换窗口时触发

# --- Api
addWidget()  # 添加窗口
removeWidget() # 移除窗口(仅仅只有移除轮播组件,如果需要销毁窗口,需要自己编写代码)
setHideButtons() # 设置隐藏/显示左右按钮(默认显示)
setAutoSlideShow() # 设置自动轮播
getWidgetCount() # 获取当前窗口的数量
getWidget() # 通过索引获取窗口
getIndex() # 获取当前索引
next()  # 切换到下一个窗口
up() # 切换到上一个窗口
getButtons() # 返回左右按钮对象(可以通过这个方法来重写左右按钮样式)
```

