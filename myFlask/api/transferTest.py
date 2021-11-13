#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time    : 2021/11/13 15:53
# @Author  : xuan
# @Site    : 
# @File    : transferTest.py
# @Software: PyCharm

from server.server import app
from flask import jsonify, request


@app.route('/transfer/json', methods=['POST'])
def transfer1():
    """
    @author:     xuan
    @create time:2021/11/13 16:24
    @desc:     post请求，接收数据为json格式，返回也为json
    """
    req = request.json
    print(req)
    res = {"result": "json", "code": 0}
    return jsonify(res)

@app.route('/transfer/args', methods=['GET'])
def transfer2():
    """
    @author:     xuan
    @create time:2021/11/13 16:26
    @desc:       get请求，获取url后缀信息，返回json格式
    """
    req = request.args
    print(req) #ImmutableMultiDict([('name', 'lixuan')])
    req = request.args.to_dict()
    print(req) #{'name': 'lixuan'}
    res = {"result": "args", "code": 0}
    return jsonify(res)

@app.route('/transfer/form', methods=['POST','GET'])
def transfer3():
    """
    @author:     xuan
    @create time:2021/11/13 16:33
    @desc:       不限制请求方式，接收为form表单形式，返回json格式
    """
    req = request.form
    print(req) #ImmutableMultiDict([('name', 'lixuan')])
    print(req.get('name')) #lixuan
    res = {"result": "form", "code": 0}
    return jsonify(res)