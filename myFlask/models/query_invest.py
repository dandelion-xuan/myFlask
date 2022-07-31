#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time    : 2022/7/31 11:35
# @Author  : xuan
# @Desc    : 
# @File    : query_invest.py
# @Software: PyCharm

from flask import jsonify, request

from util.logger import Logger
from models import database

logger = Logger("logTest").getLogger()


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


def query_product_type_profit(product_type, start_time=None, end_time=None, state=None, if_clearance_count=False):
    """
    查询某个产品类型在指定时间内收益
    state: 1只查询当前持有产品 0orNone 查询全部
    1、查询product_info表，获取某个类型所有产品productId数组
    2、遍历productId数组，调用query_product_profit，计算profit/capital累积值/
    4、计算收益率
    5、返回计算结果
    """
    logger.info("查询product_info表，获取product_type=%d类型所有产品productId数组" % product_type)
    product_ids = []
    profit = 0
    capital = 0
    current_amount = 0
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
        if not if_clearance_count:
            if not pro_data.get("if_clearance"):
                profit += pro_data.get("profit")
                capital += pro_data.get("capital")
                current_amount += pro_data.get("current_amount")
    logger.info(profit)
    logger.info(capital)

    logger.info("计算收益率")
    profit_rate = profit / capital
    logger.info(profit)

    data = {
        "product_type": product_type,
        "profit": profit,
        "profit_rate": profit_rate,
        "capital": capital,
        "current_amount": current_amount,
    }
    return data


def query_all_products_profit(start_time=None, end_time=None, state=None, if_clearance_count=False):
    """
    查询某个产品类型在指定时间内收益
    state: 1只查询当前持有产品 0orNone 查询全部
    if_clearance_count: 为False时，if_clearance 为true时需去掉；为True时不去掉。即为False时才需要处理数据
    """
    logger.info("查询product_info表，获取类型所有产品productId数组")
    product_ids = []
    if state:
        pro_sql = "select product_id from product_info where state = 1;"
    else:
        pro_sql = "select product_id from product_info;"
    pro_result = database.Database.execute(pro_sql)
    for pro_id in pro_result:
        product_ids.append(pro_id[0])
    logger.info(product_ids)

    logger.info("遍历productId数组，调用query_product_profit")
    product_data = []
    for pro_id in product_ids:
        pro_data = query_product_profit(pro_id, start_time=start_time, end_time=end_time)
        if not if_clearance_count:
            # if_clearance_count为false时需要处理数据
            if not pro_data.get("if_clearance"):
                # 如果 if_clearance 为 False时才需要添加数据
                product_data.append(pro_data)
    return product_data
