#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time    : 2022/7/23 17:55
# @Author  : xuan
# @Desc    : 
# @File    : database.py
# @Software: PyCharm
import pymysql
import time
from config import config
from util.logger import Logger


# from lib.logger import log
# from lib.errors.expection import DatabaseError

logger = Logger("logTest").getLogger()

def connect_database():
    connect_time = 5
    while connect_time:
        try:
            db = pymysql.connect(
                user=config.USER, \
                password=config.PASSWORD, \
                database=config.DATABASE, \
                host=config.HOST, \
                port=config.PORT, \
                autocommit=False
            )
            return db
        except BaseException as e:
            logger.error(str(e))
            logger.error('connect database fail, try it in 3 second....')
            # print(e)
            time.sleep(3)  # in second
        connect_time -= 1
    # raise DatabaseError('can not connect database')


class Database:
    global_db = connect_database()

    def __init__(self):
        pass

    @classmethod
    def execute(cls, sql):
        logger.debug('execute sql: {}'.format(sql))
        try:
            cls.global_db.ping(reconnect=True)
            cursor = cls.global_db.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            cls.global_db.commit()
            cursor.close()
            logger.debug(result)
            return result
        except BaseException as e:
            logger.error(str(e))
            cls.global_db.rollback()
            # raise DatabaseError("internal database error")

    @classmethod
    def get_last_insert_id(cls):
        return cls.execute('select @@IDENTITY')[0][0];
