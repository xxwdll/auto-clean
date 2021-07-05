from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def create_session():
    connect_args = { 'check_same_thread': False }
    engine       = create_engine('sqlite:///./lib/auto-clean.db', echo=False, connect_args=connect_args)
    #engine       = create_engine('sqlite:///./lib/auto-clean.db', echo=True)
    DBSession    = sessionmaker(bind=engine)
    session      = DBSession()
    return session
