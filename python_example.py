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
        <select name="name1">
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
@app.route('/add', methods=['GET', 'POST'])
def add():
    sid=request.form.get("add")
    cid = request.form.get('name1')

    # 建立資料庫連線
    conn = MySQLdb.connect(host="127.0.0.1",
                        user="hj",
                        passwd="test1234",
                        db="testdb")
    
    results = """
    <p><a href="/">回到首頁</a></p>
    """
    
    c_credit = "SELECT credit FROM elective where c_id='{}'".format(cid)   #欲選學分數
    # 執行查詢(選課學分)
    cursor = conn.cursor()
    cursor.execute(c_credit)
    for i in cursor.fetchone():
        c_credit = i
    s_credit = "SELECT total_credit FROM student where s_id='{}'".format(sid)   #已選學分數
    # 執行查詢(已選學分)
    cursor = conn.cursor()
    cursor.execute(s_credit)
    for i in cursor.fetchone():
        s_credit = i
    t_credit = s_credit + c_credit
    if t_credit > 30:
        results += '超過可選之學分'
        return results        #判斷最高學分
    
    max_count = "SELECT s_limit FROM elective where c_id='{}'".format(cid)   #最高選課人數
    # 執行查詢(最高選課人數)
    cursor = conn.cursor()
    cursor.execute(max_count)
    for i in cursor.fetchone():
        max_count = i
    cur_count = "SELECT count FROM elective where c_id='{}'".format(cid)   #目前選課人數
    # 執行查詢(目前選課人數)
    cursor = conn.cursor()
    cursor.execute(cur_count)
    for i in cursor.fetchone():
        cur_count = i
    if max_count == cur_count:
        results += '已達人數上限'
        return results 
    
    I_classId = "INSERT INTO selection() VALUES ('{}','{}');".format(sid, cid)    #插入加選代號
    # 執行查詢(選課代號)
    cursor = conn.cursor()
    cursor.execute(I_classId)
    conn.commit() #插入選課列表中
    cur_count += 1
    up_count = "UPDATE elective SET count = '{}'".format(cur_count)
    cursor = conn.cursor()
    cursor.execute(up_count)
    conn.commit() #選課人數加一
    up_credit = "UPDATE student SET total_credit = '{}'".format(t_credit)
    cursor = conn.cursor()
    cursor.execute(up_credit)
    conn.commit() #總學分改變
    results += '加選成功'
    return results


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
    <p><a href="/">回到首頁</a></p>
    """
    # 取得並列出所有查詢結果
    for (c_name, ) in cursor.fetchall():
        results += "<p>{}</p>".format(c_name)
    return results
