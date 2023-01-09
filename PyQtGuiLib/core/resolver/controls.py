from PyQtGuiLib.header import QWidget


# 控件的组成分析函数
def dumpStructure(widget :QWidget ,spaceCount=0):
    '''
        widget:控件
        spaceCount:边距
    '''
    for _ in range(spaceCount):
        print("-" ,end="")
    print("\033[34;5m[{}\033[0m".format(widget.metaObject().className()),end="")
    wObj = widget.objectName()
    if wObj:
        print(":{}".format(widget.objectName()),end="")
    else:
        print(":[]", end="")
    print("\033[34;5m]\033[0m")
    # print("[{}:{}]".format(widget.metaObject().className(), widget.objectName()))

    for ch in widget.children():
        dumpStructure(ch,spaceCount + 4)