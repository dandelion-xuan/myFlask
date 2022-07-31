#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time    : 2022/7/31 15:03
# @Author  : xuan
# @Desc    : 
# @File    : expresionTest.py
# @Software: PyCharm

if __name__ == '__main__':
    a = {
        "product_type": 1,
        "profit": 1,
        "profit_rate": 1,
        "capital": 1
    }
    b = {
        "product_type": 2,
        "profit": 1,
        "profit_rate": 1,
        "capital": 1
    }
    c = {
        "product_type": 3,
        "profit": 1,
        "profit_rate": 1,
        "capital": 1
    }
    d = {
        "product_type": 4,
        "profit": 1,
        "profit_rate": 1,
        "capital": 1
    }
    l = []
    l.append(a)
    l.append(b)
    l.append(c)
    l.append(d)
    l = [1, 2, 3, 4, 11, 22]
    for k in l:
        if k == 2:
            l.pop(k)
    print(l)