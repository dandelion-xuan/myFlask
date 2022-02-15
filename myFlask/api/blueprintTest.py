#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time    : 2022/2/15 22:24
# @Author  : xuan
# @Desc    : 
# @File    : blueprintTest.py
# @Software: PyCharm

from flask import Blueprint
from flask import request

from myFlask.server.server import app
from myFlask.util.logger import Logger

simpleLogBP = Blueprint('simple',__name__,url_prefix='/simpleLog')
helloLogBP = Blueprint('hello',__name__,url_prefix='/helloLog')

@simpleLogBP.route('/log')
def simpleLog():
    print(request.url)
    app.logger.debug(request.url)
    app.logger.debug("Info message")
    return "ok"

@helloLogBP.route('/log')
def helloLog():
    print(request.url)
    try:
        logger = Logger("logTest").getLogger()
        logger.debug(request.url)
        logger.debug("debug message")
        logger.info("info message")
        return "ok,helloLogBP"
    except Exception as e:
        return e