## QSS样式解析器

```
将原本不易操作的字符串静态样式,变为易操作的动态样式.
注:字符串静态样式值的是原本写在setStyleSheet()中的样式,这里的样式对于需要动态修改时,十分的困难,当然你可以使用正则表达式,但是你想修改特定控件下的某个样式,即便是编写正则,也会显的非常繁琐,且容易出错,而QSS样式解析器的诞生就是为了解决这一系列问题.
```

### 导入方式

`from PyQtGuiLib.styles import QssStyleAnalysis`

### 一个简单例子来演示

```python
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QPushButton,
    QLabel,
    Qt,
)
from PyQtGuiLib.styles import QssStyleAnalysis

class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)


        self.setAttribute(Qt.WA_StyledBackground,True)

        self.l = QLabel("测试标签",self)
        self.btn = QPushButton("测试按钮",self)
        self.btn.setObjectName("btn")
        self.btn2 = QPushButton("测试按钮2号",self)
        self.l.move(30, 30)
        self.btn.resize(150, 80)
        self.btn.move(80, 80)
        self.btn2.resize(100,60)
        self.btn2.move(250,80)

        '''
            解析 测试1 
        '''

        # 创建一个针对整个窗口的 QSS 解析器
        self.qss = QssStyleAnalysis(self)
        # 对窗口上所有按钮,标签设置样式
        self.qss.setQSS('''
        /*===========这是一个按钮的QSS============*/
        QPushButton{
        color: rgb(0, 255, 127);
        background-color:rgb(0, 170, 0);
        }
        /*
            这是标签的样式
        */
        QLabel{
        color: rgb(42, 55, 127);
        background-color:rgb(255, 170, 0);
        }
        ''')
        print(self.qss.toStr()) # 返回样式的原始的类型
        print(self.qss.toDict()) # 返回样式的字典类型
        
        # 更新按钮的前景色
        self.qss.selector("QPushButton").updateAttr("color","yellow")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
```

在这个例子中`QssStyleAnalysis(self)`这句话就是实例化的QSS解析器,这里的参数`self`表示的是我想要

操作窗口的样式,`setQSS()`这个方法与`setStyleSheet()`都是一样的设置一个字符串样式,在这个例子在更新了按钮`color`的值,修改完成立即生效,看起来是不是很方便

### 下面来详情介绍方法的使用

**<font color=blue>setQSS(<font color=green>qss:str</font>)</font>**

- **功能:** 设置一个字符串样式

**<font color=blue>setQSSDict(<font color=green>qss_dict:dict</font>)</font>**

- **功能:** 设置一个字典形式的样式

- ```
  {
      "QPushButton":{
           "color":"rgb(0, 255, 127)",
           "background-color":"rgb(0, 170, 0)"
        }
  }
  ```

**<font color=blue>appendQSS(<font color=green>qss:str</font>)</font>**

- **功能:** 追加一个字符串样式(如果追加样式存在的,直接融合)

**<font color=blue>appendQSSDict(<font color=green>qss_dict:dict</font>)</font>**

- **功能:** 追加一个字典形式的样式(如果追加样式存在的,直接融合)

**<font color=blue>selector(<font color=green>ang:Ang</font>)</font>**

- **功能:** 返回一个选中器的QSS对象(参数是字符串或者是数字)

- ```
  这里的选择器是值的是样式的选择器,比如:QPushButton,QLabel,#abc,QPushButton:hover,...
  这些都是选择器
  ```

- **返回值:** QSS对象

**<font color=blue>selectorKey(<font color=green>key:str</font>)</font>**

- **功能:** 根据选择器来返回QSS对象
- **返回值:** QSS对象

**<font color=blue>selectorIndex(<font color=green>i:int</font>)</font>**

- **功能:** 根据索引来返回QSS对象
- **返回值:** QSS对象

**<font color=blue>removeSelector(<font color=green>ang:Ang</font>)</font>**

- **功能:** 移除该选择器/索引下的所有样式

**<font color=blue>removeSelectorKey(<font color=green>key:str</font>)</font>**

- **功能:** 移除该选择器下的所有样式

**<font color=blue>removeSelectorIndex(<font color=green>index:int</font>)</font>**

- **功能:** 通过索引移除选择器下所有样式

**<font color=blue>isSelectKey(<font color=green>key:str</font>)</font>**

- **功能:** 判断选择器是否存在
- **返回值:** 布尔类型

**<font color=blue>toStr()</font>**

- **功能:** 返回样式的字符串形式(如果样式中有注释,则去掉注释)

**<font color=blue>toDict()</font>**

- **功能:** 返回样式的字典形式(如果样式中有注释,则去掉注释)

**<font color=blue>header()</font>**

- **功能:** 返回选择器列表

**<font color=blue>count()</font>**

- **功能：**返回控件样式的数量



### QSS对象

**<font color=blue>header()</font>**

- **功能:** 返回选择器字符串

**<font color=blue>headerSubdivision()</font>**

- **功能:** 返回一个选择器列表

- ```
  假设选择器是 QWidget #btn 是这样的写的
  那么header()返回的就是QWidget #btn
  而headerSubdivision()返回的是 [QWidget,#btn]
  ```

**<font color=blue>body()</font>**

- **功能:** 返回当前选择下面的所有样式的字符串

**<font color=blue>bodySubdivision()</font>**

- **功能:** 返回当前选取器下样式的列表形式

**<font color=blue>bodyToDict()</font>**

- **功能:** 返回当前选取器下样式的字典形式

**<font color=blue>toDict()</font>**

- **功能:** 返回当前样式的字典形式

**<font color=blue>attr(key:str)</font>**

- **功能:** 获取一个属性的值

- ```
  比如 color:red;
  attr("color")  返回的是 red
  ```

**<font color=blue>updateAttr(key:str,value:str)</font>**

- **功能:** 更新/增加一个属性

**<font color=blue>removeAttr(key:str)</font>**

- **功能:** 移除某个属性

**<font color=blue>isAttr(key:str)</font>**

- **功能:** 判断一个属性是否存在

- **返回类型:** 布尔类型

**<font color=blue>toStr()</font>**

- **功能:** 返回当前样式字符串

