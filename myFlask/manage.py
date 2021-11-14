#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time    : 2021/11/13 15:32
# @Author  : xuan
# @Site    : 
# @File    : manage.py
# @Software: PyCharm

from server.server import app
import flask_excel as excel
from api import transferTest, routeTest, flaskExcelTest, pyexcelXlsxTest, logTest, pyexcelTest
import logging

if __name__ == '__main__':
    excel.init_excel(app)
    handler = logging.FileHandler('say.log')
    app.logger.addHandler(handler)
    app.logger.info("hello")
    app.run(
        host='127.0.0.1',
        port=8889,
        debug=True
    )
