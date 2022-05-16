# -*- coding: utf-8 -*-
"""
Created on Sat May 14 12:02:39 2022

@author: tang

这个程序是修饰器文件
"""


# %% 检查输入是否为字符串迭代对象
def is_str_ls_(func):
    def wrapper(*args, **kwargs):
        ls = args[0]
        for l in ls:
            if type(l) is not str:
                raise EOFError('iteration obj is not str.')
        res = func(*args, **kwargs)
        return res

    return wrapper
