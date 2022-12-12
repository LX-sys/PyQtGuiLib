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

### 组件功能完成进度

```python
气泡窗口  ---> 99%  已经可以正常使用

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

