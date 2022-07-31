#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time    : 2022/7/23 16:28
# @Author  : xuan
# @Desc    : 
# @File    : invest_record.py
# @Software: PyCharm
import datetime
import time

from flask import jsonify, request, Blueprint

from server.server import app
from util.logger import Logger
from models import database

investBP = Blueprint('invest_record', __name__, url_prefix='/invest')
logger = Logger("logTest").getLogger()


@investBP.route('/addProduct', methods=["POST"])
def add_product():
    """
    添加产品接口。需要输入原始资金。请求成功同时写入三个表
    入参格式：
    req = {
        "productId": "",
        "productName": "",
        "productType": 0,
        "amount": 10000.00
    }
    """
    req = request.json
    logger.info(req)
    product_id = req.get("productId")
    product_name = req.get("productName")
    product_type = req.get("productType")
    amount = req.get("amount")

    insert_product_sql = "insert into product_info(product_id, product_name, product_type, state) values('%s','%s',%d,1);" % (
        product_id, product_name, product_type)
    insert_trade_sql = "insert into transaction_record(product_id, product_name, trade_date, trade_amount, trade_type) values('%s', '%s', current_time , '%f', 1);" % (
        product_id, product_name, amount)
    insert_asset_sql = "insert into asset_info(product_id, product_name, current_amount, create_time) values('%s', '%s', '%f', current_time);" % (
        product_id, product_name, amount)
    result_product = database.Database.execute(insert_product_sql)
    result_trade = database.Database.execute(insert_trade_sql)
    result_asset = database.Database.execute(insert_asset_sql)
    logger.debug(result_product)
    logger.debug(result_trade)
    logger.debug(result_asset)
    if result_product is not () or result_trade is not () or result_asset is not ():
        data = {
            'message': 'failure',
            'result': 1
        }
    else:
        data = {
            'message': 'success',
            'result': 0
        }
    return jsonify(data)


@investBP.route('/addAssetRecord', methods=['POST'])
def add_asset_record():
    """
    入参格式：
    req = {
        "productId": "",
        "productName": "",
        "amount": 10000.00
    }
    """
    req = request.json
    logger.debug(req)
    product_id = req.get("productId")
    product_name = req.get("productName")
    amount = req.get("amount")

    insert_asset_sql = "insert into asset_info(product_id, product_name, current_amount, create_time) values('%s', '%s', '%f', current_time);" % (
        product_id, product_name, amount)
    result_asset = database.Database.execute(insert_asset_sql)
    logger.debug(result_asset)
    if result_asset is not ():
        data = {
            'message': 'failure',
            'result': 1
        }
    else:
        data = {
            'message': 'success',
            'result': 0
        }
    return jsonify(data)


@investBP.route('/addTradeRecord', methods=['POST'])
def add_trade_record():
    """
    入参格式：
    req = {
        "productId": "",
        "productName": "",
        "tradeDate": "2022-7-23",
        "amount": 10000.00,
        "tradeType: 1买入 2卖出
    }
    """
    req = request.json
    logger.debug(req)
    product_id = req.get("productId")
    product_name = req.get("productName")
    amount = req.get("amount")
    trade_type = req.get("tradeType")
    if "tradeDate" not in req:
        insert_trade_sql = "insert into transaction_record(product_id, product_name, trade_date, trade_amount, trade_type) values('%s', '%s', current_time , '%f', %d);" % (
            product_id, product_name, amount, trade_type)
    else:
        trade_date = req.get("tradeDate")
        insert_trade_sql = "insert into transaction_record(product_id, product_name, trade_date, trade_amount, trade_type) values('%s', '%s', '%s' , '%f', %d);" % (
            product_id, product_name, trade_date, amount, trade_type)
    result_trade = database.Database.execute(insert_trade_sql)
    logger.debug(result_trade)
    if result_trade is not ():
        data = {
            'message': 'failure',
            'result': 1
        }
    else:
        data = {
            'message': 'success',
            'result': 0
        }
    return jsonify(data)