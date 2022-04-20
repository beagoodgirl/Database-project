#!/usr/bin/env python3
# coding=utf-8
# -*- coding: UTF-8 -*-
from flask import Flask, request
import MySQLdb

app = Flask(__name__)


@app.route('/')
def index():
    form = """
    <form method="post" action="/action" >
        輸入學號：<input name="sid">
        <input type="submit" value="查詢課程">
    </form>
    """
    form1 = """
    <form method="post" action="/add" >
        輸入學號：<input name="add">
        <select>
            <option value="1245">1245 UNIX應用與實務</option>
            <option value="1260">1260 互連網路</option>
            <option value="1261">1261 組合數學</option>
            <option value="2764">1260 人生哲學</option>
            <option value="2790">2790 音樂與人生</option>
            <option value="2812">2812 莎士比亞與電影</option>
            <option value="2921">2921 水墨造型設計</option>
            <option value="3025">3025 密碼學</option>
            <option value="3598">3598 UNIX應用與實務</option>
        </select>
        <input type="submit" value="加選">
    </form>
    """
    temp=form+form1
    return temp

# 加選
@app.route('/add')
def add():
    sid=request.form.get("add")
    cid = request.form.get("value")
    # 建立資料庫連線
    conn = MySQLdb.connect(host="127.0.0.1",
                           user="hj",
                           passwd="test1234",
                           db="testdb")
    # 欲查詢的 query 指令
    query = "INSERT INTO selection (s_id,c_id) VALUES ({},{})" .format(sid,cid) #列出課表(必修)

    # 執行查詢
    cursor = conn.cursor()
    cursor.execute(query)


# 列出已選課表
@app.route('/action', methods=['POST'])
def action():
    # 取得輸入的文字
    sid = request.form.get("sid")
    # 建立資料庫連線
    conn = MySQLdb.connect(host="127.0.0.1",
                           user="hj",
                           passwd="test1234",
                           db="testdb")
    # 欲查詢的 query 指令
    query = "SELECT c_name FROM compulsory where c_id in (SELECT c_id FROM selection where s_id= '{}');".format(sid) #列出課表(必修)

    # 執行查詢
    cursor = conn.cursor()
    cursor.execute(query)

    
    results = """
    <p><a href="/">Back to Query Interface</a></p>
    """
    # 取得並列出所有查詢結果
    for (c_name, ) in cursor.fetchall():
        results += "<p>{}</p>".format(c_name)
    return results
