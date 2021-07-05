from fastapi import APIRouter
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.sql.expression import null
from lib.auth import AuthHandler
from lib.schemas import AuthDetails, AddAppInfo, ModAppInfo
from lib.models import App
from lib.database import create_session
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.sql import and_, or_
import math


router = APIRouter()
auth_handler = AuthHandler()


@router.get('/api/query_app', tags=['applist'])
async def get_app_list(page_index: int,
                       page_size: int,
                       query: str,
                       query_tag: int,
                       db: Session = Depends(create_session),
                       username=Depends(auth_handler.auth_wrapper)):
    response_info = { 'data': {},
                      'meta': { 'msg': 'Get app list success', 
                                'status': 200 }}
    if query_tag == 0 or query == '' or query_tag == 3:
        try:
            count      = db.query(func.count(App.app_id)).scalar()
            total_page = math.ceil(count/page_size)
        except Exception as e:
            response_info['meta'] = {'msg': str(e), 'status': 400 }
            return response_info
        if query_tag == 3 or page_index > total_page:
            page_index = total_page
        try:
            res = db.query(App).limit(page_size).offset(page_size*(page_index-1))
        except Exception as e:
            response_info['meta'] = {'msg': str(e), 'status': 400 }
            return response_info
    elif query_tag == 1 and query != '':
        try:
            count = db.query(func.count(App.app_id)).filter(
                        or_(App.ip.like('%'+query+'%'), 
                            App.cluster_info.like('%'+query+'%'))
                    ).scalar()
            total_page = math.ceil(count/page_size)
        except Exception as e:
            response_info['meta'] = {'msg': str(e), 'status': 400 }
            return response_info
        if page_index == -1:
            page_index = 1
        if page_index > total_page:
            page_index = total_page
        try:
            res = db.query(App).filter(
                or_(App.ip.like('%'+query+'%'), App.cluster_info.like('%'+query+'%'))
            ).limit(page_size).offset(page_size*(page_index-1))
        except Exception as e:
            response_info['meta'] = {'msg': str(e), 'status': 400 }
            return response_info
    elif query_tag == 2 and query != '':
        try:
            count = db.query(func.count(App.app_id)).filter(
                or_(App.ip == query, App.cluster_info == query)
            ).scalar()
            total_page = math.ceil(count/page_size)
        except Exception as e:
            response_info['meta'] = {'msg': str(e), 'status': 400 }
            return response_info
        if page_index == -1:
            page_index = 1
        if page_index > total_page:
            page_index = total_page
        try:
            res = db.query(App).filter(
                or_(App.ip == query, App.cluster_info == query)
            ).limit(page_size).offset(page_size*(page_index-1))
        except Exception as e:
            response_info['meta'] = {'msg': str(e), 'status': 400 }
            return response_info
    else:
        response_info['meta'] = {'msg': 'Method not found!', 'status': 404 }
        return response_info
    app_list = []
    for i in res:
        temp = {}
        temp['ip']           = i.ip
        temp['cluster_info'] = i.cluster_info
        temp['app_id']       = i.app_id
        app_list.append(temp)
    response_info['data'] = { 'total_page': total_page,
                              'total_rows': count,
                              'page_index': page_index,
                              'app_list': app_list }
    return response_info


@router.post('/api/add_app', tags=['applist'])
async def add_app(app_info: AddAppInfo, db: Session = Depends(create_session), username=Depends(auth_handler.auth_wrapper)):
    response_info = { 'data': {},
                      'meta': { 'msg': 'Add success', 
                                'status': 200 }}
    ip   = app_info.ip
    cluster_info = app_info.cluster_info
    res  = db.query(App).filter(and_(App.ip == ip, App.cluster_info == cluster_info)).all()
    if len(res) != 0:
        response_info['meta'] = { 'msg': 'Appinfo already exists!', 'status': 401 }
        return response_info
    new_app = App(ip=app_info.ip, cluster_info=app_info.cluster_info)
    try:
        db.add(new_app)
        db.commit()
    except Exception as e:
        response_info['meta'] = { 'msg': str(e), 'status': 400 }
        return response_info
    return response_info


@router.put('/api/mod_app', tags=['applist'])
async def mod_app(app_info: ModAppInfo, db: Session = Depends(create_session), username=Depends(auth_handler.auth_wrapper)):
    response_info = { 'data': {},
                      'meta': { 'msg': 'Mod success', 
                                'status': 200 }}
    ip   = app_info.ip
    cluster_info = app_info.cluster_info
    res  = db.query(App).filter(and_(App.ip == ip, App.cluster_info == cluster_info)).all()
    if len(res) != 0:
        response_info['meta'] = { 'msg': 'Appinfo already exists!', 'status': 401 }
        return response_info
    new_app = { 'ip': app_info.ip, 'cluster_info':app_info.cluster_info }
    try:
        db.query(App).filter(App.app_id == app_info.app_id).update(new_app)
        db.commit()
    except Exception as e:
        response_info['meta'] = { 'msg': str(e), 'status': 400 }
        return response_info
    return response_info

@router.delete('/api/delete_app', tags=['applist'])
async def delete_app(app_id: int, 
                     db: Session = Depends(create_session), 
                     username=Depends(auth_handler.auth_wrapper)):
    response_info = { 
                        'data': {},
                        'meta': { 'msg': 'Delete success', 'status': 200 }
                    }
    res  = db.query(App).filter(App.app_id == app_id).all()
    if len(res) == 0:
        response_info['meta'] = {'msg': 'Already delete!', 'status': 401 }
        return response_info
    try:
        db.query(App).filter(App.app_id == app_id).delete()
        db.commit()
    except Exception as e:
        response_info['meta'] = { 'msg': str(e), 'status': 400 }
        return response_info
    return response_info