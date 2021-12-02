#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time    : 2021/11/13 22:34
# @Author  : xuan
# @Site    : 
# @File    : routeTest.py
# @Software: PyCharm
from server.server import app
from flask import request, jsonify


"""
@author: xuan
@create time: 2021/11/13 23:01
@desc: 请求urlhttp://127.0.0.1:8889/，返回func hello,不返回func index
"""
@app.route('/', endpoint='index')
def hello():
    print(request.url)
    res = {"result": "in func hello", "code": 0}
    app.logger.info('req:')
    app.logger.debug("debug")
    app.logger.warning("warming")
    app.logger.error("error!")
    return jsonify(res)

def index():
    print(request.url)
    res = {"result": "in func index", "code": 0}
    return jsonify(res)

"""
@author: xuan
@create time: 2021/11/13 23:09
@desc: func+add_url_rule 与 route+视图效果一致
"""
def home():
    print(request.url)
    res = {"result": "in func home", "code": 0}
    return jsonify(res)

app.add_url_rule('/home',view_func=home)

# @app.route('/home')
# def home():
#     print(request.url)
#     res = {"result": "in func home", "code": 0}
#     return jsonify(res)

"""
@author: xuan
@create time: 2021/11/13 23:15
@desc: URL (http://www.example.org/greeting/Mark) 映射到端点"say_hello"上.
指向端点"say_hello"的请求被视图函数"give_greeting"处理.viewfunction**–>endpoint–>**URL
"""
@app.route('/greeting/<name>', endpoint='say_hello')
def give_greeting(name):
    return 'Hello, {0}!'.format(name)

"""
@author: xuan
@create time: 2021/11/13 23:24
@desc: 动态路由
类型	说明
string	默认，可以不用写
int	整数
float	同 int，但是仅接受浮点数
path	和 string 相似，但接受斜线限制。eg:string：/hello/ error; path:/hello/ true
"""
@app.route('/hello/<username>')
def sayHello(username):
    return 'hello {0}'.format(username)

@app.route('/age/<int:age>')
def myAge(age):
    return 'my age:{0},type:{1}'.format(age,type(age)) #type:int

@app.route('/path/<path:name>')
def show_path(name):
    return 'path is %s' % name