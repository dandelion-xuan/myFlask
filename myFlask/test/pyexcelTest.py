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

def excelRead(file_name):
    sh = pe.get_sheet(file_name = file_name,sheet_name = "学校", delimiter = '\t')
    print(type(sh))
    print(sh)
    # arr = pe.get_array(file_name = file_name,sheet_name = "学校", delimiter = '\t')
    arr = pe.get_array(file_name = file_name,delimiter = '\t')
    print(type(arr))
    print(arr)
    # dd = pe.get_dict(file_name = file_name,sheet_name = "学校", delimiter = '\t')
    dd = pe.get_dict(file_name = file_name, delimiter = '\t')
    print(type(dd))
    print(dd)
    print(dict(dd))
    rec = pe.get_records(file_name = file_name, delimiter = '\t')
    print(type(rec))
    print(rec)
    bk = pe.get_book(file_name = file_name)
    print(type(bk))
    print(bk)
    bkd = pe.get_book_dict(file_name = file_name)
    print(type(bkd))
    print(bkd)


if __name__ == '__main__':

    filePath = os.path.join(excel_file_path,'exampleForExcel.xlsx')
    print('filePath',filePath)

    excelRead(file_name=filePath)

    try:
        arr = pe.get_array(file_name = filePath,sheet_name = 'personal')
        print(arr[1:])
    except Exception as err:
        print(err)