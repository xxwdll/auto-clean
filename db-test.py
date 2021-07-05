#-*- coding:UTF-8 -*-
from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from sqlalchemy.orm import Session

from sqlalchemy import func
#from sqlalchemy.sql import and_,asc,desc,or_
from sqlalchemy.sql import and_, or_

Base = declarative_base()

class User(Base):
    __tablename__  = 'user_info'
    user_id        = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_name      = Column(String(20))
    user_pass      = Column(String(50))

class Cluster(Base):
    __tablename__  = 'cluster_info'    
    cluster_name   = Column(String(50))
    type_info      = Column(String(20))
    command        = Column(Text)
    auto_key       = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

def create_session():
    #engine    = create_engine( 'sqlite:///auto.db',
    #                           connect_args={"connection_factory": bytes})
    engine    = create_engine( 'sqlite:///auto.db')
    engine.raw_connection().connection.text_factory = bytes
    DBSession = sessionmaker(bind=engine)
    session   = DBSession()
    return session

class App(Base):
    __tablename__ = 'app_info'
    ip            = Column(String(50))
    cluster_info  = Column(String(100))
    app_id        = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

def dict_factory(cursor, row):
  d = {}
  for idx, col in enumerate(cursor.description):
    d[col[0]] = row[idx]
  return d

def t_sqlite(db, sql):
    import sqlite3
    conn = sqlite3.connect(db)
    conn.text_factory = bytes
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute(sql)
    res = cur.fetchall()
    print(res)
    #conn.commit()
    conn.close()
    return res

if __name__ == '__main__':
    db  = create_session()
    query = '111'
    #res = db.query(User).filter(User.user_name==user_name).first()
    #res = db.query(User).first()
    res = db.query(func.count(App.app_id)
                .filter(
                or_(App.ip.like('%'+query+'%'), App.cluster_info.like('%'+query+'%')
            )))
    count = res.scalar()
    print(count)
    page_size = 20
    page_index = 1
    # res = db.query(App).filter(
    #             or_(App.ip.like('%'+query+'%'), App.cluster_info.like('%'+query+'%'))
    #         ).limit(page_size).offset(page_size*(page_index-1))
    for i in res:
        print(i.ip)
    #sql = 'select * from app_info where cluster_info like "%nagios%";'
    #sql = 'select * form app_info where cluster_info limit 1;'
    #res = t_sqlite('auto.db', sql)
    #for i in res:
    #    try:
    #        j = i['cluster_info'].decode('utf-8')
    #    except:
    #        j = str(i['cluster_info'])
    #    print(j)
    #    print('---------------------')