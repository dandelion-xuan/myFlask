#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time    : 2021/11/14 15:52
# @Author  : xuan
# @Desc    : log模块
# @File    : logTest.py
# @Software: PyCharm

from flask import request, jsonify

from server.server import app
from util.logger import Logger

@app.route('/log')
def printLog():
    print(request.url)
    app.logger.debug(request.url)
    app.logger.debug("Info message")
    return "ok"

@app.route('/helloLog')
def printLogger():
    print(request.url)
    try:
        logger = Logger("logTest").getLogger()
        logger.debug(request.url)
        logger.debug("debug message")
        logger.info("info message")
        return "ok"
    except Exception as e:
        return e