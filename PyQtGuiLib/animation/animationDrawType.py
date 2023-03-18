# -*- coding:utf-8 -*-
# @time:2023/3/1715:33
# @author:LX
# @file:animationDrawType.py
# @software:PyCharm

'''
    这个类为绘图动画的封装类型
'''


# 值类型
class AniNumber:
    def __init__(self,n):
        self.__n = n

    def setNumber(self,n):
        self.__n = n

    def number(self)->int:
        return self.__n


# 多值类型
class AniNumbers:
    def __init__(self,*args):
        self.__an = []
        if args:
            self.setNumbers(*args)

    def setNumbers(self,*args):
        for an in args:
            self.__an.append(AniNumber(an))

    def numberObjs(self)->list:
        return [n for n in self.__an]

    def numbers(self)->tuple:
        return [n.number() for n in self.__an]