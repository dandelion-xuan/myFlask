#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time    : 2021/11/14 11:05
# @Author  : xuan
# @desc    : 安装插件：pip install Flask-Excel，Flask-Excel支持 csv, tsv, csvz, tsvz 格式.from http://flask.pyexcel.org/zh_CN/latest/index.html
# @File    : flaskExcelTest.py
# @Software: PyCharm

import flask_excel as excel
from flask import request, jsonify
from server.server import app
@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        return jsonify({"result": request.get_array(field_name='file')})
    return '''
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Excel file upload (csv, tsv, csvz, tsvz only)</h1>
    <form action="" method=post enctype=multipart/form-data><p>
    <input type=file name=file><input type=submit value=Upload>
    </form>
    '''


@app.route("/download", methods=['GET'])
def download_file():
    return excel.make_response_from_array([[1, 2], [3, 4]], "csv")


@app.route("/export", methods=['GET'])
def export_records():
    return excel.make_response_from_array([[1, 2], [3, 4]], "csv",
                                          file_name="export_data")


@app.route("/download_file_named_in_unicode", methods=['GET'])
def download_file_named_in_unicode():
    return excel.make_response_from_array([[1, 2], [3, 4]], "csv",
                                          file_name=u"中文文件名") #不加u也行，不会乱码