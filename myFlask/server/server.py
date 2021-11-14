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
# from logging import FileHandler

app = Flask(__name__)
# CORS(app, supports_credentials=True)


