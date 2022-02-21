#!/usr/bin/python
# -*- coding:utf-8 -*-
# @File  : urlforTest.py
# @Author: p_lixuanzhu
# @date 2022/2/21
import flask
from flask import url_for
from flask import request

from server.server import app
from myFlask.util.logger import Logger

logger = Logger("logTest").getLogger()
@app.route('/urlforOne',methods=['GET'])
def urlforFirst():
    logger.debug(request.url)
    return flask.redirect(url_for('urlforSecond'))

@app.route('/urlforTwo',methods=['GET'])
def urlforSecond():
    logger.info("请求我！")
    return "this is urlforTwo"

@app.route('/<page>/user',methods=['GET'])
def pageurl(id):
    logger.debug(id)
    logger.debug(request.url)
    logger.debug(request.args)
    return "this is pageurl"

@app.route('/urlpage',methods=['GET'])
def url():
    logger.debug(request.url)
    logger.debug(request.args)
    return url_for('pageurl',page=1,count=2)

@app.route('/test',methods=['GET'])
def query_user():
    '''
    http://127.0.0.1:5000/test?id=123
    '''
    id = request.args.get('id')
    return 'query user:'+id

@app.route('/query_url')
def query_url():
    '''
    反导出 query_user函数名对应的url地址
    '''
    return 'query url:'+url_for('query_user',id='123',name='小明')