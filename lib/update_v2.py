#-*- coding:UTF-8 -*-
from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy.sql import and_, or_
import time

Base = declarative_base()

class AppInfo(Base):
    __tablename__ = 'app_info'
    ip            = Column(String(50))
    cluster_info  = Column(String(100))
    app_id        = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

class AppInfoTemp(Base):
    __tablename__ = 'app_info_temp'
    ip            = Column(String(50))
    cluster_info  = Column(String(100))
    app_id        = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

class AppList(Base):
    __tablename__  = 'app_list'
    id             = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    busniess_name  = Column(String(50))
    app_name       = Column(String(100))
    app_cluster    = Column(String(100))
    app_ip         = Column(String(30))
    data_src       = Column(String(30))
    app_nameid     = Column(String(30))
    app_pgm        = Column(String(50))

class AppListTemp(Base):
    __tablename__  = 'app_list_temp'
    id             = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    busniess_name  = Column(String(50))
    app_name       = Column(String(100))
    app_cluster    = Column(String(100))
    app_ip         = Column(String(30))
    data_src       = Column(String(30))
    app_nameid     = Column(String(30))
    app_pgm        = Column(String(50))

class SysEasyOps(Base):
    __tablename__ = 'syseasyops'
    busniess_name  = Column(String(50))
    app_name       = Column(String(100), primary_key=True)
    app_cluster    = Column(String(100))
    app_ip         = Column(String(30), primary_key=True)
    app_memo       = Column(String(30))
    data_src       = Column(String(30))

class SysEasyOpsBussiness(Base):
    __tablename__ = 'syseasyopsbussiness'
    busniess_id    = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    busniess_name  = Column(String(50))
    department     = Column(String(100))
    companymemo    = Column(String(100))

class SysEasyOpsPgm(Base):
    __tablename__ = 'syseasyopspgm'
    busniess_name  = Column(String(50))
    app_name       = Column(String(100), primary_key=True)
    app_cluster    = Column(String(100), primary_key=True)
    app_pgm        = Column(String(30), primary_key=True)
    app_memo       = Column(String(30))
    app_nameid     = Column(String(30))

def time_decorator(func):
    def exec_fun(*args, **kwargs):
        t = time.perf_counter()
        result = func(*args, **kwargs)
        print("%s 执行时间: %f s" % (func.__name__, (time.perf_counter()-t)))
        return result
    return exec_fun

def create_session():
    dbname    = 'sqlite:///./lib/auto-clean.db'
    engine    = create_engine(dbname, echo=False)
    DBSession = sessionmaker(bind=engine)
    session   = DBSession()
    return session

def create_mysql_session():
    engine = create_engine("mysql+pymysql://cmdb:123456@none-ops.db.chinner.com:3306/springcmdb?charset=utf8", echo=False)
    DBSession = sessionmaker(bind=engine)
    session   = DBSession()
    return session

def create_table(table_objects):
    dbname    = 'sqlite:///./lib/auto-clean.db'
    engine    = create_engine(dbname, echo=False)
    table_objects = [table_objects.__table__]
    Base.metadata.create_all(engine, tables=table_objects)
    #Base.metadata.tables["AppInfoTemp"].create(bind=engine)

def drop_table(table_objects):
    dbname    = 'sqlite:///./lib/auto-clean.db'
    engine    = create_engine(dbname, echo=False)
    table_objects = [table_objects.__table__]
    Base.metadata.drop_all(engine, tables=table_objects)

@time_decorator
def get_mysql_data():
    temp_table_name = AppListTemp
    db = create_mysql_session()
    counts = []
    for _ in range(3):
        res = db.query(SysEasyOps.busniess_name,
              SysEasyOps.app_name,
              SysEasyOps.app_cluster,
              SysEasyOps.app_ip,
              SysEasyOps.data_src,
              SysEasyOpsPgm.app_nameid,
              SysEasyOpsPgm.app_pgm).join(
              SysEasyOpsPgm,
              and_(
                   SysEasyOps.busniess_name==SysEasyOpsPgm.busniess_name,
                   SysEasyOps.app_name==SysEasyOpsPgm.app_name
                  )
              ).filter(SysEasyOpsPgm.app_nameid!='None').distinct().all()
        counts.append(len(res))
    if counts[0] != counts[1] or counts[1] != counts[2]:
        return None
    db.close()
    drop_table(temp_table_name)
    create_table(temp_table_name)
    db = create_session()
    while res:
        exec_list = []
        task = 50
        if len(res) < task:
            task = len(res)
        for _ in range(task):
            data = res.pop(0)
            data = temp_table_name(busniess_name = data.busniess_name,
                                   app_name = data.app_name,
                                   app_cluster = data.app_cluster,
                                   app_ip = data.app_ip,
                                   data_src = data.data_src,
                                   app_nameid = data.app_nameid,
                                   app_pgm = data.app_pgm)
            exec_list.append(data)
        db.add_all(exec_list)
        db.commit()
        db.close()
    return 'success'

@time_decorator
def compare_table():
    table_A = AppList
    table_B = AppListTemp
    create_table(table_A)
    create_table(table_B)
    db = create_session()
    count1 = len(db.query(table_A).join(table_B,
                 and_(
                     table_A.app_ip==table_B.app_ip,
                     table_A.app_nameid==table_B.app_nameid
                 )
             ).all())
    res = db.query(table_B).all()
    if count1 == len(res):
        return 'pass'
    drop_table(table_A)
    create_table(table_A)
    while res:
        exec_list = []
        task = 50
        if len(res) < task:
            task = len(res)
        for _ in range(task):
            data = res.pop(0)
            data = table_A(busniess_name = data.busniess_name,
                           app_name = data.app_name,
                           app_cluster = data.app_cluster,
                           app_ip = data.app_ip,
                           data_src = data.data_src,
                           app_nameid = data.app_nameid,
                           app_pgm = data.app_pgm)
            exec_list.append(data)
        try:
            db.add_all(exec_list)
            db.commit()
        except:
            return None
    return 'update success'

@time_decorator
def check_and_innsert():
    source_table = AppList
    table_A      = AppInfo
    table_B      = AppInfoTemp
    db = create_session()
    create_table(table_A)
    drop_table(table_B)
    create_table(table_B)
    res = db.query(source_table).all()
    while res:
        exec_list = []
        task = 50
        if len(res) < task:
            task = len(res)
        for _ in range(task):
            data = res.pop(0)
            data = table_B(ip = data.app_ip,
                           cluster_info = str(data.app_name) + str(data.app_cluster)
                   )
            exec_list.append(data)
        try:
            db.add_all(exec_list)
            db.commit()
        except:
            return None
    res = db.query(table_B.ip, table_B.cluster_info).outerjoin(table_A, 
                   and_(
                        table_A.ip==table_B.ip,
                        table_A.cluster_info==table_B.cluster_info
                   )
          ).filter(table_A.ip==None).all()
    if len(res) == 0:
        return 'pass'
    while res:
        exec_list = []
        task = 50
        if len(res) < task:
            task = len(res)
        for _ in range(task):
            data = res.pop(0)
            data = table_A(ip = data.ip,
                           cluster_info = data.cluster_info
                   )
            exec_list.append(data)
        try:
            db.add_all(exec_list)
            db.commit()
        except:
            return None
    return 'update success'

def main():
    res = get_mysql_data()
    if res == None:
        return
    res = compare_table()
    if res == None:
        return
    res = check_and_innsert()
    if res == None:
        return
    if res == 'pass':
        print('数据无更新，忽略!')
        return
    print(res)
    print('数据已更新!')

if __name__ == '__main__':
    main()
