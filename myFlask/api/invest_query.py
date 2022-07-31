#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time    : 2022/7/31 11:50
# @Author  : xuan
# @Desc    : 
# @File    : invest_query.py
# @Software: PyCharm
import datetime
import time

from flask import jsonify, request, Blueprint

from server.server import app
from util.logger import Logger
from models import database
from models import query_invest

investBP2 = Blueprint('invest_query', __name__, url_prefix='/invest')
logger = Logger("logTest").getLogger()


@investBP2.route('/view_1', methods=['POST'])
def view_1():
    """
    @create time: 2022/7/31 11:39
    @author: xuan
    @desc: 不同产品收益、收益率、资产对比。不包括现仍持有产品清仓记录的
    :param
    :startTime
    :endTime
    return
    """
    req = request.json
    logger.info(req)
    startTime = req.get("startTime")
    endTime = req.get("endTime")
    data = {
        'message': 'success',
        'result': 0
    }
    resinfo = query_invest.query_all_products_profit(start_time=startTime, end_time=endTime, state=1)
    if resinfo:
        data["info"] = resinfo
    else:
        data = {
            'message': 'failure',
            'result': 1
        }
    return jsonify(data)


@investBP2.route('/view_3', methods=['POST'])
def view_3():
    """
    @create time: 2022/7/31 11:39
    @author: xuan
    @desc: 不同性质产品收益、收益率、资产对比。不包括现仍持有产品清仓记录的
    :param
    :startTime
    :endTime
    """
    req = request.json
    logger.info(req)
    startTime = req.get("startTime")
    endTime = req.get("endTime")
    product_types = []
    resInfo = []
    data = {
        'message': 'success',
        'result': 0
    }
    logger.info("查询product_info表，获取所有产品类型数组")
    pro_sql = "select product_type from product_info where state = 1;"
    pro_result = database.Database.execute(pro_sql)
    for pro_type in pro_result:
        product_types.append(pro_type[0])
    logger.info(product_types)
    for i in product_types:
        resinfo = query_invest.query_product_type_profit(product_type=i, start_time=startTime, end_time=endTime, state=1)
        resInfo.append(resinfo)
    data["info"] = resInfo
    return jsonify(data)


@investBP2.route('/view_5', methods=['POST'])
def view_5():
    """
    @create time: 2022/7/31 11:39
    @author: xuan
    @desc: 所有操作买卖记录表
    :param
    :startTime
    :endTime
    """
    req = request.json
    startTime = req.get("startTime")
    endTime = req.get("endTime")

    print("遍历所有产品，查询 transaction_record 表，获取其交易记录，以及计算总投入钱")
    records = []
    trade_amount = 0
    record_sql = "select * from transaction_record where trade_type=1 and trade_date between '%s' and '%s';" % (startTime, endTime)
    record_sql_result = database.Database.execute(record_sql)
    for tur in record_sql_result:
        record = {
            "id": tur[0],
            "product_id": tur[1],
            "product_name": tur[2],
            "trade_date": tur[3],
            "trade_amount": tur[4],
        }
        records.append(record)
        trade_amount += tur[4]

    data = {
        'message': 'success',
        'result': 0,
        'records': records,
        "trade_amount": trade_amount,
        "startTime": startTime,
        "endTime": endTime
    }
    return jsonify(data)


@investBP2.route('/view_6', methods=['POST'])
def view_6():
    """
    @create time: 2022/7/31 11:39
    @author: xuan
    @desc: 收益、赚的钱（落袋为安）
    :param
    :startTime
    :endTime
    """
    req = request.json
    startTime = req.get("startTime")
    endTime = req.get("endTime")

    print("遍历所有产品，查询 transaction_record 表，获取其交易记录，以及计算总投入钱")
    records = []
    trade_amount = 0
    record_sql = "select * from transaction_record where trade_type=2 and trade_date between '%s' and '%s';" % (startTime, endTime)
    record_sql_result = database.Database.execute(record_sql)
    for tur in record_sql_result:
        record = {
            "id": tur[0],
            "product_id": tur[1],
            "product_name": tur[2],
            "trade_date": tur[3],
            "trade_amount": tur[4],
        }
        records.append(record)
        trade_amount += tur[4]

    data = {
        'message': 'success',
        'result': 0,
        'records': records,
        "trade_amount": trade_amount,
        "startTime": startTime,
        "endTime": endTime
    }
    return jsonify(data)