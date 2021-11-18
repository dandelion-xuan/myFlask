#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time    : 2021/11/14 22:03
# @Author  : xuan
# @Desc    : 
# @File    : __init__.py.py
# @Software: PyCharm


import os,sys
root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
print("root_path:",root_path)
data_path = os.path.join(root_path,'data')
print("data_path:",data_path)
excel_file_path = os.path.join(data_path,'excelTestData')
print("excel_file_path:",excel_file_path)