#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time    : 2021/11/13 15:32
# @Author  : xuan
# @Site    : 
# @File    : manage.py
# @Software: PyCharm

# import flask_excel as excel

from server.server import app, logging_handler
from api import logTest
from api.blueprintTest import simpleLogBP, helloLogBP
from api.invest import investBP

if __name__ == '__main__':
    # excel.init_excel(app)
    app.logger.addHandler(logging_handler)
    app.register_blueprint(simpleLogBP)
    app.register_blueprint(helloLogBP)
    app.register_blueprint(investBP)

    app.run(
        host='127.0.0.1',
        port=8889,
        debug=True
    )
