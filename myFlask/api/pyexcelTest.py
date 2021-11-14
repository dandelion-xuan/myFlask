#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time    : 2021/11/14 15:39
# @Author  : xuan
# @Desc    : 
# @File    : pyexcelTest.py
# @Software: PyCharm

from flask import request, jsonify
import pyexcel as pe
from pyexcel.cookbook import merge_all_to_a_book
import glob
#导入自定义文件
from server.server import app
from util import today
from config import excel_file_path
file_name = excel_file_path + "\exampleForExcel.xlsx"
# file_name = r"..\data\excelTestData\exampleForExcel.xlsx"
@app.route('/excel/read')
def excel_read():
    """
    @desc: 只有get_book和get_book_dict能显示所有的sheet，其他需要指定sheet_name，否则默认为第一个sheet
    @create time: 2021/11/14 20:33
    @author:
    """
    print(request.url)
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
    return 'OK'

@app.route('/excel')
def excelGetDict():
    """
    @desc: https://blog.csdn.net/lb245557472/article/details/103050957,
    @create time: 2021/11/14 21:27
    @author: xuan
    """
    sh = pe.get_sheet(file_name = file_name,sheet_name = "学校", delimiter = '\t')
    print(sh[0,0])
    print(sh.row[0])
    print(sh.column[0])
    print(sh.number_of_rows())
    print(sh.number_of_columns())
    print(sh.content)
    sheet = pe.get_sheet(file_name=file_name, name_columns_by_row=0)
    # 列名
    print(list(sheet.colnames))
    # 数据以字典格式读出
    print(sheet.to_dict())
    print(dict(sheet.to_dict()))

    # 按行获取数据，不包括headers
    print(list(sheet.rows()))
    # 反序
    print(list(sheet.rrows()))

    # 按列获取数据，不包括headers
    print(list(sheet.columns()))
    # 反序
    print(list(sheet.rcolumns()))

    # 数据扁平化，放在一个list中
    print(list(sheet.enumerate()))
    print(list(sheet.reverse()))
    print(list(sheet.vertical()))
    print(list(sheet.rvertical()))
    extra_data = [["Column 4", "Column 5"], [10, 13],
                  [11, 14], [12, 15], [12, 15]]
    sheet2 = pe.Sheet(extra_data)
    sheet.column += sheet2
    print(sheet.content)

    import pyexcel as p

    # 写book
    content = {
        'Sheet_1':
            [
                [1.0, 2.0, 3.0],
                [4.0, 5.0, 6.0],
                [7.0, 8.0, 9.0]
            ],
        'Sheet_2':
            [
                ['X', 'Y', 'Z'],
                [1.0, 2.0, 3.0],
                [4.0, 5.0, 6.0]
            ],
        'Sheet_3':
            [
                ['O', 'P', 'Q'],
                [3.0, 2.0, 1.0],
                [4.0, 3.0, 2.0]
            ]
    }
    book = p.get_book(bookdict=content)
    book.save_as("output.xlsx")
    # 读book
    book = p.get_book(file_name="output.xlsx")
    sheets = book.to_dict()
    for name in sheets.keys():
        print(name)

    print(book.sheet_by_name("Sheet_1"))
    print(book.Sheet_1)
    print(book["Sheet_1"])
    return 'OK'

@app.route('/excel/io')
def excel_io():
    """
    @desc: 
    @create time: 2021/11/14 22:11
    @author: xuan
    """
    dest_file_name = excel_file_path + r"\arrWrite.xlsx"
    arr = []
    arr.append([today,'SIT1',"ao_vb_marketing_act_server","test_query_auto_task","我也不知道为什么啊","那就这样吧"])
    arr.append([today,'SIT2',"ao_vb_marketing_act_server","test_query_auto_task","我也不知道为什么啊","那就这样吧"])
    pe.save_as(array = arr, dest_file_name = dest_file_name, sheet_name = "晴雨表")
    results = pe.get_sheet(file_name=dest_file_name)
    print(results)
    #写入多个sheet，使用bookdict
    dest_file_name = excel_file_path + "\写入多个sheet.xlsx"
    bkd = {}
    sheets = ["晴雨表","跟进表","结果表"]
    for sheet in sheets:
        bkd[sheet] = arr
    pe.save_book_as(bookdict = bkd, dest_file_name = dest_file_name)
    results = pe.get_book(file_name = dest_file_name)
    print(results)
    return 'OK'

@app.route('/excel/merge')
def excel_merge():
    """
    @desc: 将目录中的所有excel文件合并到一个文件中，每个文件成为一个工作表.https://blog.csdn.net/lb245557472/article/details/103050957
    @create time: 2021/11/14 22:32
    @author: xuan
    """
    merge_file = excel_file_path + "\merge.xlsx"
    merge_all_to_a_book(filelist=glob.glob(excel_file_path + "/*.xlsx"),outfilename=merge_file)
    return 'OK'
