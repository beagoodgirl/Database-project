#!/usr/bin/env python3
# coding=utf-8
# -*- coding: UTF-8 -*-
from flask import Flask, request, render_template, session, redirect, url_for
import MySQLdb

# 建立資料庫連線
conn = MySQLdb.connect(host="127.0.0.1",
                        user="hj",
                        passwd="test1234",
                        db="testdb")

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/')
def index():
    return render_template("login.html")


@app.route('/home')
def home():
    return render_template('home.html', username = session['username'])

@app.route('/login',methods=['GET', 'POST'])
def login():
    
    msg=''
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        user = "SELECT * FROM username WHERE username = '{}' and password = '{}'".format(username, password)
        cursor = conn.cursor()
        cursor.execute(user)
        record = cursor.fetchone()
        if record:
            session['logged'] = True
            session['username'] = record[0]
            return redirect(url_for('home'))
        else:
            msg='帳號/密碼有誤，請再次嘗試'
            return msg
    return render_template("login.html")
            
        
@app.route('/logout')
def logout():
    session.pop('logged', None)
    session.pop('username', None)
    return redirect(url_for('login'))  


#將必修直接加入已選課表
@app.route('/compulsory' , methods=['POST'])
def compulsory():
    # 建立資料庫連線
    conn = MySQLdb.connect(host="127.0.0.1",
                        user="hj",
                        passwd="test1234",
                        db="testdb")

    compulsory_count = 0
    c = "SELECT c_id FROM compulsory where dept_grade = 2"
    cursor = conn.cursor()
    cursor.execute(c)
    s = "SELECT s_id FROM student where 2022-register_year = 2"
    cursor1 = conn.cursor()
    cursor1.execute(s)
    g = "SELECT credit FROM compulsory where dept_grade = 2"
    cursor2 = conn.cursor()
    cursor2.execute(s)
    
    for (i, ) in cursor.fetchall:
        for (j, ) in cursor1.fetchall:
            com ="INSERT INTO selection() VALUES ('{}','{}');".format(j,i)
            cursor3 = conn.cursor()
            cursor3.execute(com)
            conn.commit() #插入選課列表中
            compulsory_count += 1

            c_count = "UPDATE compulsory SET count = '{}' where c_id = '{}'".format(compulsory_count,i) 
            cursor4 = conn.cursor()
            cursor4.execute(c_count)
            conn.commit() #人數+1

            total_credit = "SELECT total_credit FROM student where s_id = '{}'".format(j)
            cursor5 = conn.cursor()
            cursor5.execute(total_credit)
            for k in  cursor5.fetchone():
                total_credit = k
                total_credit += g #計算總學分
            
            save_total_credit = "UPDATE student SET total_credit = '{}' where s_id = '{}'".format(total_credit,j) 
            cursor6 = conn.cursor()
            cursor6.execute(save_total_credit)
            conn.commit() #總學分加回去

        compulsory_count = 0

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
    <p><a href="/home">回到首頁</a></p>
    """

    # 判斷是否選過
    sel = "SELECT count(*) FROM selection where c_id='{}' and s_id = '{}'".format(cid,sid)
    cursor = conn.cursor()
    cursor.execute(sel)
    for i in cursor.fetchone():
        sel = i
    if sel != 0:
        results += '這堂課選過了'
        return results


    #判斷超修
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
        return results   #判斷最高學分
    
    # 判斷人數已滿
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
    
    #課程名稱重複
    class_name_select = "SELECT c_name FROM elective where c_id = '{}'".format(cid) #查詢課程名稱
    # 執行查詢(目前課程名稱)
    cursor = conn.cursor()
    cursor.execute(class_name_select)

    for i in cursor.fetchone():
        class_name_select = i 

    class_name_elective = "SELECT c_name FROM elective where c_id != '{}'".format(cid)
    # 執行查詢(所有課程名稱)
    cursor1 = conn.cursor()
    cursor1.execute(class_name_elective)

    already = "SELECT c_id FROM selection where s_id = '{}'".format(sid)
    cursor2 = conn.cursor()
    cursor2.execute(already)

    for (i, ) in cursor1.fetchall():
        for (j, ) in cursor2.fetchall():
            if class_name_select == i and cid != j:
                results += '選到重覆課程!!!'
                return results

    # #判斷是否衝堂
    # already_select = "SELECT count(*) FROM selection where c_id = '{}'".format(cid)
    # cursor = conn.cursor()
    # cursor.execute(already_select)
    # for i in cursor.fetchone():
    #     already_select=i

    # if(i)
    # class_time = "SELECT slot FROM course_time where c_id = '{}'".format(cid)
    # cursor1 = conn.cursor()
    # cursor1.execute(class_time)

    # all_class_time = "SELECT slot FROM course_time where c_id != '{}'".format(cid)
    # cursor2 = conn.cursor()
    # cursor2.execute(all_class_time)

    # for (i, ) in cursor1.fetchall():
    #     for (j, ) in cursor2.fetchall():
    #         if i == j :
    #             results += '衝堂，加選失敗'
    #             return results        

    #加選成功，人數及學分加一
    I_classId = "INSERT INTO selection() VALUES ('{}','{}');".format(sid, cid)    #插入加選代號
    # 執行查詢(選課代號)
    cursor = conn.cursor()
    cursor.execute(I_classId)
    conn.commit() #插入選課列表中
    cur_count += 1
    up_count = "UPDATE elective SET count = '{}' where c_id = '{}'".format(cur_count,cid)
    cursor = conn.cursor()
    cursor.execute(up_count)
    conn.commit() #選課人數加一
    up_credit = "UPDATE student SET total_credit = '{}' where s_id = '{}'".format(t_credit,sid)
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
    query_compulsory = "SELECT c_name FROM compulsory where c_id in (SELECT c_id FROM selection where s_id= '{}');".format(sid) #列出課表(必修)
    # 執行查詢
    cursor = conn.cursor()
    cursor.execute(query_compulsory)
    query_elective = "SELECT c_name FROM elective where c_id in (SELECT c_id FROM selection where s_id= '{}');".format(sid) #列出課表(必修)
    # 執行查詢
    cursor1 = conn.cursor()
    cursor1.execute(query_elective)
    
    results = """
    <p><a href="/home">回到首頁</a></p>
    """
    # 取得並列出所有查詢結果
    for (c_name, ) in cursor.fetchall():
        results += "<p>{}</p>".format(c_name)
    for (i, ) in cursor1.fetchall():
        results += "<p>{}</p>".format(i)
    return results 




    # 退選
@app.route('/quit', methods=['GET', 'POST'])
def quit():
    sid=request.form.get("del")
    cid = request.form.get('name2')
    # 建立資料庫連線
    conn = MySQLdb.connect(host="127.0.0.1",
                        user="hj",
                        passwd="test1234",
                        db="testdb")
    results = """
    <p><a href="/home">回到首頁</a></p>
    """
    # 欲查詢的總學分指令
    s_credit = "SELECT total_credit FROM student WHERE s_id='{}'".format(sid)
    #執行查詢(已選學分)
    cursor = conn.cursor()
    cursor.execute(s_credit)
    for i in cursor.fetchone():
        s_credit = i
    # 欲查詢的是否為必修指令 (利用join與學分去判斷)
    com_id = "SELECT c_id FROM compulsory WHERE c_id='{}'".format(cid)
    co_id = 0      #先把co_id歸零(必修id)
    c_credit = 0    #課程的學分先歸零
    count = 0
    cursor = conn.cursor()
    cursor.execute(com_id)
    for j in cursor.fetchall():
        if cid == j[0]:
            for i in cursor.fetchone():
                co_id += i     #假如為必修，id則放入co_id
                com_credit = "SELECT credit FROM compulsory WHERE c_id='{}'".format(cid)
                cursor = conn.cursor()
                cursor.execute(com_credit)
                for i in cursor.fetchone():
                    com_credit = i     #假如為必修，此課程學分放入com_credit
                if com_credit > 0:
                    c_credit = com_credit
                count += 1
                break
                
    if count == 0 :
        # 欲查詢的是否為選修指令
        ele_id = "SELECT c_id FROM elective WHERE c_id='{}'".format(cid)
        cursor = conn.cursor()
        cursor.execute(ele_id)
        e_id = 0      #先把e_id歸零(必修id)
        for i in cursor.fetchone():
            e_id += i
            ele_credit = "SELECT credit FROM elective WHERE c_id='{}'".format(cid)
            cursor = conn.cursor()
            cursor.execute(ele_credit)
            for i in cursor.fetchone():
                ele_credit = i     #假如為選修，此課程學分放入ele_credit
            if e_id > 0:
                c_credit = ele_credit
    
    t_credit ="SELECT total_credit FROM student WHERE s_id='{}'".format(sid)
    cursor = conn.cursor()
    cursor.execute(t_credit)
    for i in cursor.fetchone():
        t_credit = i
    t_credit -= c_credit      #若退選完的總計的學分
    
    if t_credit < 9:
        results += '將低於最低學分'
        return results
    elif co_id > 0:
        results += "<p>退選必修課程</p>"
        del1 = "DELETE FROM selection where s_id='{}' and c_id='{}'".format(sid, cid) #刪除課表
        cursor = conn.cursor()
        cursor.execute(del1)
        conn.commit()
        results += "<p>退選成功</p>"
    else:
        del2 = "DELETE FROM selection where s_id='{}' and c_id='{}'".format(sid, cid) #刪除課表
        cursor = conn.cursor()
        cursor.execute(del2) 
        conn.commit()
        results += "<p>退選成功</p>"
        
    update1 = "UPDATE student SET total_credit = '{}' WHERE s_id='{}'".format(t_credit, sid) #更新退選完後的學分
    cursor.execute(update1)
    conn.commit()
    return results
