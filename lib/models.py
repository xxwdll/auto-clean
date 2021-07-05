#from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class User(Base):
    __tablename__  = 'user_info'
    user_id        = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_name      = Column(String(20))
    user_pass      = Column(String(50))


class Script(Base):
    __tablename__ = 'cluster_info'
    cluster_name = Column(String(50))
    type_info    = Column(String(50))
    command      = Column(Text)
    auto_key     = Column(Integer, primary_key=True, nullable=False, autoincrement=True)


class App(Base):
    __tablename__ = 'app_info'
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

class Menu(Base):
    __tablename__ = 'menu_info'
    menu_id       = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    menu_name     = Column(String(50))
    father_id     = Column(Integer)
    menu_level    = Column(Integer)
    menu_path     = Column(String(50))


class ScriptTemp(Base):
    __tablename__ = 'script_temp'
    id            = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    # value       = Column(Integer, nullable=False, autoincrement=True)
    label         = Column(String(50))
    command       = Column(Text)


class AlarmInfo(Base):
    __tablename__ = 'alarm_info'
    id            = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    ip            = Column(String(25))
    start_time    = Column(DateTime, nullable=False)
    end_time      = Column(DateTime, nullable=False)
    spend_time    = Column(Integer)
    path          = Column(String(25))
    clean_space   = Column(Integer)
    disk_percent  = Column(String(25))