# -*- coding:utf-8 -*-
# @time:2023/3/2717:33
# @author:LX
# @file:logBrowser.py
# @software:PyCharm
from PyQtGuiLib.header import (
    QApplication,
    sys,
    PYQT_VERSIONS,
    QWidget,
    QTextBrowser,
    QThread,
    Signal,
    QObject,
    QScrollBar,
    QListWidget
)
import os
import time
from datetime import datetime as dt


TimeFormat = str


class SendLog(QThread):
    send = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# 计算日志大小线程
class LogSizeTh(QThread):
    Sizeed = Signal(int)

    def __init__(self, path:str):
        super().__init__()
        self.__path = path

    def setPath(self,path):
        self.__path = path

    def run(self):
        st = os.stat(self.__path)
        self.Sizeed.emit(st.st_size)


# 本地日志管理
class LoadLocalLog(QThread):
    loaded = Signal(str)
    finish = Signal()

    def __init__(self, path=".",filename="test.txt",encoding="utf8",limit=1000):
        super().__init__()
        self.__local_log = {
            "path": path,
            "filename": filename
        }
        self.__encoding = encoding
        self.__limit = limit

    def setLimit(self,n:int):
        self.__limit = n

    def limit(self)->int:
        return self.__limit

    def encoding(self) -> str:
        return self.__local_log

    def setLocalFileInfo(self, path, filename):
        self.__local_log["path"] = path
        self.__local_log["filename"] = filename

    def localFileInfo(self) -> dict:
        return self.__local_log

    def path(self) -> str:
        return self.__local_log["path"]

    def fileName(self) -> str:
        return self.__local_log["filename"]

    def run(self):
        old = time.time()
        print("开始:",old)
        path = os.path.join(self.path(),self.fileName())
        with open(path,"r") as f:
            n = 0
            size = 0
            limit = self.limit()
            while n<limit or limit == -1:
                data = f.readline()
                if data:
                    size += len(data)
                    self.loaded.emit(data)
                    # self.msleep(1)
                else:
                    break
                n += 1
        print("数据量:{} 字节大小:{}".format(n,size))
        new = time.time()
        print("耗时:",new-old)
        self.finish.emit()

# 日志控件
class LogBrowser(QTextBrowser):
    Debug = "Debug"
    Info = "Info"
    Warning = "Warning"
    Error = "Error"
    Critical = "Critical"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.__timeFormat = "%Y-%m-%d %H:%M:%S"
        self._start_slider_value = 0
        self._next_slider_value = 0


        self.log_size = LogSizeTh(r"D:\code\PyQtGuiLib\PyQtGuiLib\core\logBrowser\test.txt")
        self.log_size.Sizeed.connect(lambda n:print("日志大小:",n))
        self.log_size.start()

        self.ll = LoadLocalLog(limit=1000)
        self.ll.loaded.connect(self.test)
        self.ll.finish.connect(self.init_slider_event)
        self.ll.start()
        self.verticalScrollBar().sliderMoved.connect(self.info)

    # 在第一次加载日志后,初始化滚动条
    def init_slider_event(self):
        self.verticalScrollBar().setValue(0)
        self._start_slider_value = self.verticalScrollBar().value()
        self._next_slider_value = self.verticalScrollBar().value()

    def sliderValue(self) -> int:
        return self.verticalScrollBar().value()

    def wheelEvent(self, *args, **kwargs):
        self._next_slider_value = self.sliderValue()
        print(self._start_slider_value,self._next_slider_value)
        if self._next_slider_value > self._start_slider_value:
            print("向下")
        elif self._next_slider_value < self._start_slider_value:
            print("向上")

        self._start_slider_value = self._next_slider_value
        super().wheelEvent(*args,**kwargs)

    def info(self,i):
        print(i)

    def test(self,info):
        self.append(info,LogBrowser.Debug)

    def setTimeFormat(self,format:TimeFormat):
        self.__timeFormat = format

    def timeFormat(self) -> TimeFormat:
        return self.__timeFormat

    def append(self, p_str,mode="Info"):
        for_time = dt.strftime(dt.now(),self.timeFormat())
        log = "{mode} [{time}] > {info}".format(mode=mode,
                                            time=for_time,
                                            info=p_str.replace("\n",""))
        super().append(log)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = LogBrowser()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())

