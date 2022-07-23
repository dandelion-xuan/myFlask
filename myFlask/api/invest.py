#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time    : 2022/7/23 16:28
# @Author  : xuan
# @Desc    : 
# @File    : invest.py
# @Software: PyCharm
import datetime
import time

from flask import jsonify, request, Blueprint

from server.server import app
from util.logger import Logger
from models import database

investBP = Blueprint('invest', __name__, url_prefix='/invest')
logger = Logger("logInvest").getLogger()


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
    logger.debug(req)
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


def query_product_profit(product_id, start_time=None, end_time=None):
    """
    查询每个产品在指定时间内收益
    return:profit_amount, if_clearance(产品收益金额，是否清仓)
    收益 = 当前资产 + 已卖出 - 成本
    成本 = 买入 + 上次资产
    收益率 = 收益/成本
    当前资产：查询资产表时间范围内最新一条记录。如果资产=0，if_clearance=True
    已卖出：查询交易记录表时间范围内卖出金额总和
    买入：查询交易记录表时间范围内买入金额总和
    上次资产：查询资产表时间小于start_time且最新的一条记录。
    """
    if_clearance = False
    logger.info("获取当前资产")
    current_amount_sql = "select current_amount from asset_info where product_id = '%s' and create_time between '%s' and '%s' order by create_time desc limit 1;" % (
        product_id, start_time, end_time)
    current_amount_result = database.Database.execute(current_amount_sql)
    current_amount = current_amount_result[0][0]
    if not current_amount:
        if_clearance = True
    logger.info(current_amount)

    logger.info("获取上次资产")
    eariest_amount_sql = "select current_amount from asset_info where product_id = '%s' and create_time < '%s' order by create_time desc limit 1;" % (
        product_id, start_time)
    eariest_amount_result = database.Database.execute(eariest_amount_sql)
    if eariest_amount_result is ():
        eariest_amount = 0
    else:
        eariest_amount = eariest_amount_result[0][0]
    logger.info(eariest_amount)

    logger.info("获取已卖出金额")
    back_amout_sql = "select sum(trade_amount) from transaction_record where product_id = '%s' and trade_type = 2 and trade_date between '%s' and '%s';" % (
        product_id, start_time, end_time)
    back_amout_result = database.Database.execute(back_amout_sql)
    if not back_amout_result[0][0]:
        back_amout = 0
    else:
        back_amout = back_amout_result[0][0]
    logger.info(back_amout)

    logger.info("获取成本")
    purchase_sql = "select sum(trade_amount) from transaction_record where product_id = '%s' and trade_type = 1 and trade_date between '%s' and '%s';" % (
        product_id, start_time, end_time)
    purchase_result = database.Database.execute(purchase_sql)
    purchase = purchase_result[0][0]
    logger.info(purchase)
    capital = eariest_amount + purchase
    logger.info(capital)

    logger.info("计算收益和收益率")
    profit = current_amount + back_amout - capital
    logger.info(profit)
    profit_rate = profit / capital
    logger.info(profit_rate)

    data = {
        "product_id": product_id,
        "profit": profit,
        "profit_rate": profit_rate,
        "if_clearance": if_clearance,
        "capital": capital,
        "current_amount": current_amount,
        "back_amout": back_amout
    }
    return data


@investBP.route('/test', methods=['POST'])
def query_product_type_profit():
# def query_product_type_profit(product_type, start_time=None, end_time=None, state=None):
    """
    查询某个产品类型在指定时间内收益
    state: 1只查询当前持有产品 0orNone 查询全部
    1、查询product_info表，获取某个类型所有产品productId数组
    2、遍历productId数组，调用query_product_profit，计算profit/capital累积值/
    4、计算收益率
    5、返回计算结果
    """
    req = request.json
    product_type = req.get("productType")
    start_time = req.get("start_time")
    end_time = req.get("end_time")
    if "state" in req:
        state = req.get("state")
    else:
        state = None

    logger.info("查询product_info表，获取product_type=%d类型所有产品productId数组" % product_type)
    product_ids = []
    profit = 0
    capital = 0
    if state:
        pro_sql = "select product_id from product_info where product_type = %d and state = 1;" % product_type
    else:
        pro_sql = "select product_id from product_info where product_type = %d;" % product_type
    pro_result = database.Database.execute(pro_sql)
    for pro_id in pro_result:
        product_ids.append(pro_id[0])
    logger.info(product_ids)

    logger.info("遍历productId数组，调用query_product_profit，计算profit/capital累积值")
    for pro_id in product_ids:
        pro_data = query_product_profit(pro_id, start_time=start_time, end_time=end_time)
        profit += pro_data.get("profit")
        capital += pro_data.get("capital")
    logger.info(profit)
    logger.info(capital)

    logger.info("计算收益率")
    profit_rate = profit / capital
    logger.info(profit)

    data = {
        "product_type": product_type,
        "profit": profit,
        "profit_rate": profit_rate,
        "capital": capital
    }
    return jsonify(data)
