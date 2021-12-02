#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time    : 2021/11/13 15:36
# @Author  : xuan
# @Site    : 
# @File    : server.py
# @Software: PyCharm

from flask import Flask
from flask_cors import CORS
import logging

# CORS(app, supports_credentials=True)

import logging
from logging.handlers import RotatingFileHandler

# 默认日志等级的设置
logging.basicConfig(level=logging.DEBUG)

logging_handler = logging.FileHandler(filename='app.log',encoding='UTF-8')
logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
logging_handler.setFormatter(logging_format)

app = Flask(__name__)

