from fastapi import APIRouter
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.sql.expression import null
from lib.auth import AuthHandler
from lib.schemas import AuthDetails, ResetPass
from lib.models import User, App, Menu, Script
from lib.database import create_session
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.sql import and_, or_
import math


router = APIRouter()
auth_handler = AuthHandler()


@router.get('/api', tags=['userlist'])
async def get_users(db: Session = Depends(create_session)):
    count = db.query(func.count(App.app_id)).scalar()
    res   = db.query(App).limit(100)
    app_list = []
    for i in res:
        temp = {}
        temp['ip']           = i.ip
        temp['cluster_info'] = i.cluster_info
        temp['app_id']       = i.app_id
        app_list.append(temp)
    return { 'data' : app_list, 'count': count }


@router.post('/api/register', status_code=201, tags=['userlist'])
async def register(auth_details: AuthDetails, db: Session = Depends(create_session)):
    #session = create_session
    data = {}
    meta = {}
    user = db.query(User).filter(User.user_name==auth_details.username).first()
    if user:
        #raise HTTPException(status_code=400, detail='Username is taken')
        meta['msg']    = 'Username is taken'
        meta['status'] = 400
        return { 'data': data, 'meta': meta }
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    new_user = User(user_name=auth_details.username, user_pass=hashed_password)
    try:
        db.add(new_user)
        db.commit()
    except Exception as e:
        meta['msg']    = str(e)
        meta['status'] = 400
        return { 'data': data, 'meta': meta }
    meta['msg']    = 'register succsess'
    meta['status'] = 200
    return { 'data': data, 'meta': meta }


@router.post('/api/login', tags=['userlist'])
async def login(auth_details: AuthDetails, db: Session = Depends(create_session)):
    data = {}
    meta = {}
    user = db.query(User).filter(User.user_name==auth_details.username).first()
    if (user is None) or (not auth_handler.verify_password(auth_details.password, user.user_pass)):
        #raise HTTPException(status_code=401, detail='Invalid username and/or password')
        meta['msg']    = 'Invalid username and/or password'
        meta['status'] = 401
        return { 'data': data, 'meta': meta }
    token = auth_handler.encode_token(user.user_name)
    meta['msg']      = 'login success'
    meta['status']   = 200
    data['id']       = user.user_id
    data['username'] = user.user_name
    data['token']    = 'Bearer ' + token
    return { 'data': data, 'meta': meta }


@router.post('/api/reset_password', tags=['userlist'])
async def reset_password(
                         _info: ResetPass, 
                         db: Session = Depends(create_session),
                         username=Depends(auth_handler.auth_wrapper)
                        ):
    response_info = { 
                      'data': {},
                      'meta': { 
                                'msg': 'Reset Password success', 
                                'status': 200
                              }
                    }                    
    user = db.query(User).filter(User.user_name==username).first()
    if (user is None) or (not auth_handler.verify_password(_info.password, user.user_pass)):
        #raise HTTPException(status_code=401, detail='Invalid username and/or password')
        response_info['meta'] = { 
                                 'msg': 'Invalid username and/or password',
                                 'status': 401
                                }
        return response_info
    hashed_password = auth_handler.get_password_hash(_info.newpassword)
    new_user = { 'user_pass': hashed_password }
    try:
        db.query(User).filter(User.user_id == user.user_id).update(new_user)
        db.commit()
    except Exception as e:
        response_info['meta'] = { 'msg': str(e), 'status': 400 }
        return response_info
    return response_info