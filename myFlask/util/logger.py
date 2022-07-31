#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time    : 2022/2/13 16:29
# @Author  : xuan
# @Desc    : 
# @File    : logger.py
# @Software: PyCharm

import logging
from logging import handlers


class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射

    def __init__(self, filename, level='debug', backupCount=10):
        logPath = 'logs/'
        logName = logPath + filename
        print(logName)
        formatStr = logging.Formatter('[%(asctime)s] [%(name)s-%(funcName)s] [%(levelname)s]: %(message)s')
        self.logger = logging.getLogger(logName)
        self.logger.setLevel(self.level_relations.get(level))
        # 创建一个handler，用于将日志输出到控制台
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(formatStr)
        if not self.logger.handlers:
            # 创建一个handler，用于写入日志文件 , 往文件里写入#指定间隔时间自动生成文件的处理器
            fileHandler = handlers.TimedRotatingFileHandler(filename=logName, when="midnight", backupCount=backupCount,
                                                            encoding='utf-8')
            fileHandler.setFormatter(formatStr)

            # self.logger.addHandler(consoleHandler)
            self.logger.addHandler(fileHandler)

    def getLogger(self):
        return self.logger
