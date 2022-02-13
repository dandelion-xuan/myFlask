#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time    : 2021/11/13 15:32
# @Author  : xuan
# @Site    : 
# @File    : manage.py
# @Software: PyCharm

import flask_excel as excel

from server.server import app,logging_handler
from api import logTest


if __name__ == '__main__':
    excel.init_excel(app)
    app.logger.addHandler(logging_handler)


    app.run(
        host='127.0.0.1',
        port=8889,
        debug=True
    )
