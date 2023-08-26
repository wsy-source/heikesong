import pymssql
from flask import session
import random
from datetime import datetime


# Obtain connection string information from the portal
def get_conn():
    try:
        connect = pymssql.connect(
            server='heikemalasong.database.windows.net',
            user='psql',
            password='Azure1234',
            database='db',
            charset='utf8',
            as_dict=True
        )
        print("-----------------------------------")
        print("Connection Established")
        print(connect)
        return {"conn": connect, "code": 200}
    except Exception as e:
        print(e)
        return {"error": e, "code": 400}


# Insert Articles
def addArticles(title, author, doi, url, user_id, abstract):
    print("addArticles")
    conn = get_conn()
    try:
        current_time = datetime.now()
        cursor = conn["conn"].cursor()
        cursor.execute(
            "insert into Articles (title, author, doi, url, created_at, updated_at, user_id, abstract) values(%s, %s, %s, %s, %s, %s, %s, %s)",
            (title, author, doi, url, current_time, current_time, user_id, abstract))
        print("sql 语句执行成功")
        print("Insert", cursor.rowcount, "row(s) of data.")
        conn["conn"].commit()
        return {"code": 200, "Msg": "Added Successed"}
    finally:
        cursor.close()
        conn["conn"].close()


# 查文献列表
def searchArticles(title, author, abstract):
    conn = get_conn()
    try:
        print("++++++++++4444444444444444++++++++++++++")
        cursor = conn["conn"].cursor()

        # LOWER(title) like '%{}%' ".format(a.LOWER())
        # OFFSET 20 ROWS
        # FETCH NEXT 10 ROWS ONLY;   【sql server中没有limit关键字】
        # 不区分大小写查询 WHERE title COLLATE SQL_Latin1_General_CP1_CI_AI LIKE '%abcd%'

        sql = "SELECT id, title, doi, url, author,abstract, ai_abstract FROM Articles"
        sqlSplice = ""
        if title:
            sqlSplice = sqlSplice + "and title COLLATE SQL_Latin1_General_CP1_CI_AI LIKE '%{}%'".format(title)
        if author:
            sqlSplice = sqlSplice + "and author COLLATE SQL_Latin1_General_CP1_CI_AI LIKE '%{}%'".format(author)
        if abstract:
            sqlSplice = sqlSplice + "and (abstract COLLATE SQL_Latin1_General_CP1_CI_AI LIKE '%{}%' or ai_abstract COLLATE SQL_Latin1_General_CP1_CI_AI LIKE '%{}%')".format(
                abstract, abstract)

        if sqlSplice:
            newSplice = sqlSplice.replace("and", "", 1)
            print(newSplice)
            sql = sql + " where " + newSplice + " ORDER BY created_at DESC"
            # 如果分页 ↓
            # page = 2
            # count = 10
            # sql = sql + " where " + sqlSplice + " ORDER BY created_at DESC" + "OFFSET {%s} ROWS".format((page-1)*10) + "FETCH NEXT {%d} ROWS ONLY".format(count)
        else:
            sql = sql + " ORDER BY created_at DESC"
            # 如果分页 ↓
            # page = 2
            # count = 10
            # sql = sql + " ORDER BY created_at DESC" + " ORDER BY created_at DESC" + "OFFSET {%s} ROWS".format((page-1)*10) + "FETCH NEXT {%d} ROWS ONLY".format(count)
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn["conn"].close()
