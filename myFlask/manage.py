#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time    : 2021/11/13 15:32
# @Author  : xuan
# @Site    : 
# @File    : manage.py
# @Software: PyCharm

from server.server import app
from api import transferTest, routeTest


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=8889,
        debug=True
    )
