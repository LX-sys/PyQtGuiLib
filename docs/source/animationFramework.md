# 动画框架

### 说明

```
Animation是一个基于原生的动画基础上封装的一套简单易用型框架,可以对普通的控件添加动画,
也可以对控件的QSS属性添加动画,还能给画师所绘制的图形添加动画.
```

### 导入方式

`from PyQtGuiLib.animation import Animation`

### 一个简单列子来演示

```python
from PyQtGuiLib.header import (
    QApplication,
    PYQT_VERSIONS,
    sys,
    QWidget,
    QPushButton,
    QRect,
    QPoint
)

# 动画框架
from PyQtGuiLib.animation import Animation

class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)
        '''
             Animation 动画框架 案例一,移动一个按钮
        '''

        self.btn = QPushButton("按钮",self)
        self.btn.move(50,50)
        self.btn.resize(100,60)

        # 实例化动画类
        self.ani = Animation(self)
        # 设置动画时长
        self.ani.setDuration(2000) # 2秒

        # 对按钮添加移动动画
        '''
            addAni() 这个方法是一个非常常用的函数,用于添加一个动画
            参数是一个json格式,
            这里使用的参数含义
            targetObj:表示动画的作用对象
            propertyName: 动画的动作
            sv:起始值
            ev:结束值
        '''
        self.ani.addAni({
            "targetObj": self.btn,
            "propertyName": b"pos", # pos动作 是表示移动
            "sv": self.btn.pos(),
            "ev": QPoint(300,100)
        })
        # 开始动画
        self.ani.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
```

从这个例子不难看出`addAni()`这个方法是用来添加与动画相关的参数的,<font color=red>**targetObj**</font>这个参数表示需要添加动画的对象,<font color=red>**propertyName**</font>表示动画具体要执行的动作,<font color=red>**sv和ev**</font>则表示动画的起始值和结束值,不同的动作,这里的值则不同.

### 目前所支持的参数

```python
targetObj: 需要添加的动画对象,一般情况下这个参数都是必填项,只有有绘图时,不需要这个参数
    
propertyName:btype 动画的执行动作,必填项
    -- 普通控件常用的动作 geometry,size,pos,windowOpacity
    --- 支持绝大部分QSS属性动作,例如(background-color,color,...)
    --- value 这个动作比较特殊,一般只有在绘图动画才会使用
    
duration:int 动画执行的时间,可选参数(默认1000,就是1秒)
special: 动画的曲线参数,可选参数,内置了4种曲线(InCurve, OutBounce, CosineCurve, SineCurve) 
loop:int 动画循环次数,可选参数(默认1次)
    
call:fun 回调函数参数,可以在动画执行完成,调用一次,回调函数必须有一个参数 可选参数
argc:tuple 回调函数的参数 可选参数
  
sv: 动画的起始值,在大多数情况下可以写成"this"来指向自己当
atv:[()] 或者 [] 动画的插值  可选参数
ev: 动画的结束值
    
selector:str 选择器参数,在对QSS属性添加动画时,这个参数是必须的,其他情况可不写
qss-suffix:"px" qss属性单位 如果: 写宽度时单位是px,表示文字大小时,有时候会用到pt,ex  可选参数
        
comment:str  备注信息  可选参数

blendFlag:True/False 混合动画标志,表示在混合模式下这类动作是串行的  可选参数
    
# -------------------
注意 sv,atv,ev 中的值的参数类型必须一致
普通控件动画最简化版
{
    "targetObj":xx,
    "propertyName":"",
    "sv":xx,
    "ev":xx
}
QSS属性动画的最简化版
{
    "targetObj":xx,
    "propertyName":"",
    "sv":xx,
    "ev":xx,
    "selector":xx
}
绘图动画最简化版
{
    "propertyName":"",
    "sv":xx,
    "ev":xx
}
```

### 常用添加动画的函数

#### <font color=blue>addAni(<font color=green>ani_data:dict</font>)</font>

- **功能**: 添加一个动画

- **ani_data**: 动画的相关参数字典

#### <font color=blue>addAnis(<font color=green>*argc</font>)</font>

- **功能**: 添加多个`addAni()`动画
- **argc**: 多个动画的相关参数字典

#### <font color=blue>addSeriesAni(<font color=green>ani_data: dict, variation: list</font>)</font>

- **功能**: 添加连续动画

- **ani_data**: 动画相关参数

- **variation**: 包含连续`ev`这个连续变化参数

- ```
  例子演示
  ani_data={
  "targetObj": xxx,
  "propertyName":b"pos",
  "sv":QPoint(0,0),
  "ev":QPoint(50,50)
  }
  variation = [QPoint(80,80),QPoint(100,100),QPoint(0,0)]
  
  类似这样的参数,值得注意的是variation中的每一个参数值,都必须和"ev"值的类型一致
  ```

#### <font color=blue>addValuesAni(<font color=green>ani_data: dict, startObj: AniStartType, ends: AniEndType</font>)</font>

- **功能**: 添加一个绘图动画
- **ani_data**: 动画的相关参数字典
- **startObj**: 特殊的对象类型,具体的说明请看后面的介绍
- **ends**:特殊的对象类型,具体的说明请看后面的介绍

#### <font color=blue>addBlend(<font color=green>ani_datas: list</font>)</font>

- **功能**: 添加多个动画,来组成混合模式动画
- **ani_datas**: 多个动画参数字典,如果参数中有`"blendFlag"=True`,则视为串行动画(默认并行动画),后面在具体介绍

#### <font color=blue>start()</font>

- **功能**: 运行动画

#### <font color=blue>state()</font>

- **功能**: 动画当前状态

#### <font color=blue>pause()</font>

- **功能**: 暂停动画

#### <font color=blue>resume()</font>

- **功能**: 恢复动画

#### <font color=blue>getAni(<font color=green>index:int</font>)</font>

- **功能**: 获取所有已经添加的动画
- **返回值类型**: List[PropertyAnimation]

#### <font color=blue>getCommentAni(<font color=green>comment:str</font>)</font>

- **功能**: 根据备注信息获取动画
- **返回值类型**: List[PropertyAnimation]

#### <font color=blue>updateAni(<font color=green>ani:PropertyAnimation,new_datas:dict</font>)</font>

- **功能**: 更新单个动画的信息
- **new_datas**: 新的动画参数,参数只需要写,你想更新的部分,对原有的其他参数不会有影响

#### <font color=blue>removeAni(<font color=green>index:int</font>)</font>

- **功能**: 移除一个动画
- **index**:索引/下标

