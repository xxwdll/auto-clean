#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import pymysql
import sqlite3
import sys, time

def time_decorator(func):
  def exec_fun(*args, **kwargs):
    t = time.perf_counter()
    result = func(*args, **kwargs)
    print("function %s coast time:%f s" % (func.__name__, (time.perf_counter()-t)))
    return result
  return exec_fun

def dict_factory(cursor, row):
  d = {}
  for idx, col in enumerate(cursor.description):
    d[col[0]] = row[idx]
  return d
class MySqlTools:
  def __init__(self, dbtype, **db_conf):
    self.dbtype = dbtype
    self.db_conf = db_conf
    if dbtype == 'mysql':
      db = db_conf.get('db', None)
      passwd = db_conf.get('passwd', None)
      if db == None or passwd == None:
        print('mysql need define db, passwd!')
        sys.exit(1)
      host = db_conf.get('host', 'localhost')
      user = db_conf.get('user', 'root')
      port = db_conf.get('port', 3306)
      charset = db_conf.get('cherset', 'utf8')
      conn = pymysql.connect(host=host,\
             user=user,\
             passwd=passwd,\
             db=db,\
             port=port, \
             charset=charset)
    elif dbtype == 'sqlite':
      db = db_conf.get('db', None)
      if db == None:
        print('sqlite need define db!')
        sys.exit(1)
      conn = sqlite3.connect(db)
      conn.text_factory = str
      conn.row_factory = dict_factory
    self.conn = conn
  def select(self, t_sql):
    if self.dbtype == 'mysql':
      cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
    elif self.dbtype == 'sqlite':
      cur = self.conn.cursor()
    try:
      cur.execute(t_sql)
    except Exception as e:
      print(e)
      return 'fail'
    result_of_sql = cur.fetchall()
    cur.close()
    return result_of_sql
  def exec(self, t_sql):
    if self.dbtype == 'mysql':
      cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
    elif self.dbtype == 'sqlite':
      cur = self.conn.cursor()
    try:
      cur.execute(t_sql)
      self.conn.commit()
    except Exception as e:
      self.conn.rollback()
      print(e)
      return 'fail'
    cur.close()
    return 'success'
  def close(self):
    self.conn.close()