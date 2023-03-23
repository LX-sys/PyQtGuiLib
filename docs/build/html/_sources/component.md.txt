# 组件文档

### 说明

```
这里包含所有自定义的组件
```

### SlideShow(轮播组件)

- 导入方式: `from PyQtGuiLib.core import SlideShow`

- ```
  信号: changeWidget
  说明: 切换窗口时触发
  ```

- ```
  类变量
  Ani_Left
  Ani_Right
  Ani_Down
  Ani_Up
  说明:动画方向模式类变量
  ```

### <font color=blue>addWidget(<font color=green>widget:QWidget</font>)</font>

- **功能**: 添加一个窗口到轮播组件

- **widget**:  一个QWidget窗口,或者是继承与QWidget的窗口

### <font color=blue>setCurrentIndex(<font color=green>index:int=0</font>)</font>

- **功能**: 切换到指定窗口
- **index**: 窗口索引(默认切换到0)

### <font color=blue>setAinDirectionMode(<font color=green>mode:tuple</font>)</font>

- **功能**: 设置窗口动画模式

- **mode**: 这个参数必须包含两种模式

- ```
  (SlideShow.Ani_Left,SlideShow.Ani_Right)
  例如这种,左右切换模式
  还有其他组合模式,请自行尝试,但是并不是所有的组合一定是正确的
  ```

### <font color=blue>setAutoSlideShow(<font color=green>b:bool,interval=1500,direction_:str="R"</font>)</font>

- **功能**: 设置自动轮播

- **b**: 是否启动自动轮播

- **interval**: 每次轮播的时间间隔

- **direction_**: 轮播的方向

- ```
  R 表示 右或者下
  L 表示 左或者上
  轮播的方向会受到动画模式下影响
  ```

### <font color=blue>removeWidget(<font color=green>widget:QWidget</font>)</font>

- **功能**: 移除窗口
- **widget**: 轮播组件上的窗口对象

### <font color=blue>getButtons()</font>

- **功能**: 获取左右可点击按钮的对象
- **返回值**: tuple

### <font color=blue>setButtonsHide(<font color=green>b:bool</font>)</font>

- **功能**: 隐藏左右可点击按钮
- **b**: 是否隐藏

### <font color=blue>count()</font>

- **功能**: 返回窗口的数量
- **返回值**: int

### <font color=blue>getWidget(<font color=green>index:int</font>)</font>

- **功能**: 通过索引获取窗口
- **返回值**: QWidget对象

