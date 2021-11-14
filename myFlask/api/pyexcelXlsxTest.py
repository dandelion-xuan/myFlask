#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time    : 2021/11/14 12:07
# @Author  : xuan
# @Desc    : 使用模块：pyexcel_xlsx
# @File    : pyexcelXlsxTest.py
# @Software: PyCharm

from server.server import app
from pyexcel_xlsx import save_data, get_data

filePath = '../data/excelTestData'

@app.route('/get_data')
def getXlsxData():
    return get_data("D:\code\myFlask\data\excelTestData\exampleForPyexcel_xlsx.xlsx",decoding = 'utf-8')

@app.route('/save_data')
def saveXlsxData():
    data = {
  "friends": [
    [
      "boyfriend",
      "bestfriends"
    ],
    [
      "Mr wu",
      "Mrs zhou"
    ]
  ],
  "personal": [
    [
      "name",
      "age",
      "hobbit"
    ],
    [
      "lixuan",
      24,
      "eat"
    ]
  ]
    }
    save_data("D:\code\myFlask\data\excelTestData\exampleForPyexcel_write_xlsx.xlsx", data=data)
    return "ok"