# -*- coding:utf-8 -*-
# @time:2023/2/813:18
# @author:LX
# @file:styleAnalysis.py
# @software:PyCharm

'''

    QSS 样式解析器
'''
from PyQtGuiLib.header import (
    SyntaxError,
    KeyError,
    QMutex
)
import typing
import re

Ang = typing.TypeVar("Any",str,int)

def dictTostr(qss_dict)->str:
    combination = ""
    for selector, attribute in qss_dict.items():
        combination += selector + "{\n"
        for attrk, attrv in attribute.items():
            combination += "%s:%s;\n" % (attrk, attrv)
        combination += "}\n"
    return combination


class Qss:
    def __init__(self,qss:str,qs=None,parent=None):
        self.__parent =parent
        self.__qs = qs

        self._qss_str = self.uncomment(qss)
        self._qss_dict = dict()
        self._qss_header = ""
        self._qss_body = ""

        self.Init()

    # Uncomment information
    def uncomment(self,qss:str) -> str:
        return re.sub("/\*.*?\*/","",qss,flags=re.DOTALL)

    def Init(self):
        header = re.findall(".*{", self._qss_str, re.DOTALL)
        if header:
            self._qss_header = header[0].replace("\n", "").replace("{", "").strip()
        else:
            raise SyntaxError("Syntax error, missing {")

        # ---
        body = re.findall(r"{(.*)}", self._qss_str, re.DOTALL)
        if body:
            self._qss_body = body[0].strip()
        self._qss_dict = {self.header(): self.bodyToDict()}

    def header(self)->str:
        return self._qss_header

    def headerSubdivision(self)->list:
        if "," in self.header():
            return self.header().split(",")
        return self.header().split(" ")

    def body(self)->str:
        return self._qss_body

    def bodySubdivision(self)->list:
        bodysub_list = []

        for v in self.body().split(";"):
            if v:
                bodysub_list.append(v.strip())
        return bodysub_list

    def bodyToDict(self)->dict:
        s_dict = dict()
        for v in self.bodySubdivision():
            key,value = v.split(":",1)
            s_dict[key]=value.strip()
        return s_dict

    def toDict(self)->dict:
        return self._qss_dict

    def attr(self,key:str)->str:
        if key in self.bodyToDict():
            return self.bodyToDict()[key]
        else:
           raise KeyError("Without this attribute,'%s'" % key)

    def updateAttr(self,key:str,value:str):
        self._qss_dict[self.header()][key]=value
        self._qss_str = dictTostr(self._qss_dict)
        self.Init()
        if self.__parent:
            self.__qs.updateStyleSheet()

    def removeAttr(self,key:str):
        if key in self._qss_dict[self.header()]:
            del self._qss_dict[self.header()][key]
            self._qss_str = dictTostr(self._qss_dict)
            self.Init()
            if self.__parent:
                self.__qs.updateStyleSheet()
        else:
            raise TypeError("Without this attribute,'%s'"%key)

    def isAttr(self,key:str)->bool:
        if self._qss_dict[self.header()].get(key):
            return True
        return False

    def toStr(self)->str:
        return self._qss_str

    def __str__(self):
        return self._qss_str


class QssStyleAnalysis:
    def __init__(self,parent=None):
        self.__parent = parent
        self._qss = [] # type:[Qss]
        # map
        self._map_qss = dict()
        self._reverse_map_qss = dict()

        self.__mutex = QMutex()  # Thread lock

    def setParent(self,parent):
        self.__parent = parent

    def parent(self):
        return self.__parent

    # Decompose multiple groups of QSS
    def groupDecomposition(self,styles):
        re_styles=re.findall(r".*?}", styles, re.DOTALL)
        if not re_styles: #
            '''
                Deal with special circumstances:
                        color: rgb(0, 255, 127);
                        background-color:rgb(0, 170, 0);
            '''
            str_p = str(type(self.__parent))
            if "QtWidgets" in str_p:
                head = re.findall("QtWidgets\.(.*)\'",str_p)
            else:
                head = re.findall("\.(.*)\'",str_p)

            re_styles = [head[0]+"{"+styles+"}"]

        return [v.strip() for v in re_styles]

    def count(self) -> int:
        return len(self._qss)

    def setQSS(self,qss:str):
        # Preprocessing qss
        self._qss = [Qss(qss,self,self.__parent) for qss in self.groupDecomposition(qss)]
        # Mapping coordinate
        self.__mappCoordinate(0,self.count())

        if self.__parent:
            self.__updateStyle(self.__parent)

    # Bidirectional mapping
    def __mappCoordinate(self,s,e):
        for i in range(s,e):
            self._map_qss[self.selectorIndex(i).header()] = i
            self._reverse_map_qss[str(i)] = self.selectorIndex(i).header()

    # Inherits styles that have been set elsewhere
    def inherit(self):
        self.setQSS(self.__parent.styleSheet())

    def setQSSDict(self,qss_dict:dict):
        self.setQSS(dictTostr(qss_dict))

    def appendQSS(self,qss:str):
        new_qss = [Qss(qss,self,self.__parent) for qss in self.groupDecomposition(qss)]
        '''
            Handle attribute fusion when the appended attribute conflicts with the original attribute
        '''
        # temp_hear = []
        for qss in new_qss:
            if self.isSelectKey(qss.header()):
                for attr,value in self.toDict()[qss.header()].items():
                    if qss.isAttr(attr) is False:
                        qss.updateAttr(attr, value)

        # del temp_hear
        old_count = self.count()
        self._qss.extend(new_qss)

        # remap
        self.__mappCoordinate(old_count,self.count())
        if self.__parent:
            self.__updateStyle(self.__parent)

    def appendQSSDict(self,qss_dict:dict):
        self.appendQSS(dictTostr(qss_dict))

    def selectorKey(self,key:str)->Qss:
        return self.selectorIndex(self._map_qss[key])

    def selectorIndex(self,i:int)->Qss:
        return self._qss[i]

    def selector(self,ang:Ang)->Qss:
        if isinstance(ang,int):
            return self.selectorIndex(ang)
        elif isinstance(ang,str):
            return self.selectorKey(ang)
        else:
            raise TypeError("Parameter error!")

    def removeSelectorIndex(self,index:int):
        self._qss.remove(self._qss[index])
        self.updateStyleSheet()
        select_name = self._reverse_map_qss[str(index)]
        del self._map_qss[select_name]
        del self._reverse_map_qss[str(index)]

        # Rebidirectional mapping
        self.__mappCoordinate(0,self.count())

    def removeSelectorKey(self,key:str):
        self.removeSelectorIndex(self._map_qss[key])

    def removeSelector(self,ang:Ang):
        if isinstance(ang, int):
            return self.removeSelectorIndex(ang)
        elif isinstance(ang, str):
            return self.removeSelectorKey(ang)
        else:
            raise TypeError("Parameter error!")

    def isSelectKey(self,key:str):
        if self._map_qss.get(key,-1)>=0:
            return True
        return False

    def toDict(self)->dict:
        qss_dict = dict()
        for i in range(self.count()):
            qss_dict.update(self.selectorIndex(i).toDict())
        return qss_dict

    def header(self)->list:
        return list(self.toDict().keys())

    def toStr(self)->str:
        return dictTostr(self.toDict())

    def __updateStyle(self, parent):
        # Thread safety
        self.__mutex.lock()
        parent.setStyleSheet("")
        parent.setStyleSheet(self.toStr())
        parent.update()
        self.__mutex.unlock()

    # updata QSS
    def updateStyleSheet(self,ang=None,parent=None):
        if ang is None:
            ang = self._qss[0].header()
        if parent is None and self.__parent is None:
            raise TypeError("Cannot update without a parent class!")
        elif parent:
            pass
            # self.selector(ang)
        elif self.__parent:
            parent = self.__parent
            # self.selector(ang)

        self.__updateStyle(parent)

    def __str__(self):
        return self.toStr()