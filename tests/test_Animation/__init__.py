# -*- coding:utf-8 -*-
# @time:2023/3/716:00
# @author:LX
# @file:__init__.py.py
# @software:PyCharm
def info(f):
    def wapper(*args,**kwargs):
        print("标记")
        f(*args,**kwargs)
    return wapper


def add_info(cls):
    for key,v in cls.__dict__.items():
        if "test" in key and callable(v):
            f = info(v)
            setattr(cls,key,f)
    return cls


@add_info
class A:
    def __init__(self):
        pass

    def test_aa(self):
        print("test")

    def test2_bb(self):
        print("test2")


a = A()
a.test_aa()
a.test2_bb()