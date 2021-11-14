#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time    : 2021/11/14 15:52
# @Author  : xuan
# @Desc    : log模块
# @File    : logTest.py
# @Software: PyCharm

from server.server import app
from flask import request, jsonify

@app.route('/log')
def printLog():
    print(request.url)
    app.logger.debug(request.url)
    app.logger.debug("Info message")
    return "ok"