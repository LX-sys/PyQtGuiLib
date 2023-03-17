# -*- coding:utf-8 -*-
# @time:2023/3/1715:33
# @author:LX
# @file:animationDrawType.py
# @software:PyCharm

'''
    这个类为绘图动画的封装类型
'''

class AniNumber:
    def __init__(self,n):
        self.__n = n

    def setNumber(self,n):
        self.__n = n

    def number(self)->int:
        return self.__n
