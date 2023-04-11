### SuperPainter

**SuperPainter**(超级画师),这个类保留原本**QPainter**类的所有功能,<font color=blue>提供的样式的私有属性</font>,并且新增了一个全新的概念,**虚拟对象**,原本**QPainter**所绘制的图形并不具备任何属性,但是**虚拟对象**的诞生可以让这些图形都变成一个个具有属性的`类`,让图形k可以在`paintEvent`这个方法之外,具有查看,修改的能力.

