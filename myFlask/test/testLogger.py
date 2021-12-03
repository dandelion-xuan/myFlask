#!/usr/bin/python
# -*- coding:utf-8 -*-
# @File  : testLogger.py
# @Author: p_lixuanzhu
# @date 2021/12/3

import logging
import logging.handlers
import datetime,time
import os,sys

test_root_path = os.path.abspath(os.path.dirname(__file__))
test_log_path = os.path.join(test_root_path,'testlog_%s.log' % time.strftime('%Y%m',time.localtime(time.time())))

testLogger = logging.getLogger('testLogger')
testLogger.setLevel(logging.DEBUG)

"""
# 调用模块时,如果错误引用，比如多次调用，每次会添加Handler，造成重复日志，这边每次都移除掉所有的handler，后面在重新添加，可以解决这类问题
while logger.hasHandlers():
    for i in logger.handlers:
        logger.removeHandler(i)
"""

rf_handler = logging.handlers.TimedRotatingFileHandler(test_log_path,encoding='utf-8', when='midnight', interval=1, backupCount=7, atTime=datetime.time(0, 0, 0, 0))
rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

f_handler = logging.FileHandler(os.path.join(test_root_path,'error.log'))
f_handler.setLevel(logging.ERROR)
f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

testLogger.addHandler(rf_handler)
# testLogger.addHandler(f_handler)

# if __name__ == '__main__':
#
#     testLogger.debug('debug message')
#     testLogger.info('info message')
#     testLogger.warning('warning message')
#     testLogger.error('error message')
#     testLogger.critical('critical message')