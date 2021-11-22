#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time    : 2021/11/22 21:43
# @Author  : xuan
# @Desc    : 
# @File    : pyexcelTest.py
# @Software: PyCharm

import pyexcel as pe
import os
#自定义方法
from myFlask.config import excel_file_path

if __name__ == '__main__':

    filePath = os.path.join(excel_file_path,'exampleForExcel.xlsx')
    print('filePath',filePath)

    try:
        arr = pe.get_array(file_name = filePath,sheet_name = 'personal')
        print(arr[1:])
    except Exception as err:
        print(err)