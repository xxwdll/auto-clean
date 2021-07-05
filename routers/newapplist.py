from fastapi import APIRouter
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import null
from lib.auth import AuthHandler
from lib.schemas import AuthDetails, AddAppList, ModAppList
from lib.models import AppList
from lib.database import create_session
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.sql import and_, or_
import math


router = APIRouter()
auth_handler = AuthHandler()


@router.get('/query_applist')
async def get_applist(page_index: int,
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
            count      = db.query(func.count(AppList.id)).scalar()
            total_page = math.ceil(count/page_size)
        except Exception as e:
            response_info['meta'] = {'msg': str(e), 'status': 400 }
            return response_info
        if query_tag == 3 or page_index > total_page:
            page_index = total_page
        try:
            res = db.query(AppList).limit(page_size).offset(page_size*(page_index-1))
        except Exception as e:
            response_info['meta'] = {'msg': str(e), 'status': 400 }
            return response_info
    elif query_tag == 1 and query != '':
        try:
            count = db.query(func.count(AppList.id)).filter(
                        or_(
                            AppList.busniess_name.like('%'+query+'%'),
                            AppList.app_name.like('%'+query+'%'),
                            AppList.app_cluster.like('%'+query+'%'),
                            AppList.app_ip.like('%'+query+'%'),
                            AppList.app_nameid.like('%'+query+'%'),
                            AppList.app_pgm.like('%'+query+'%')
                            )
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
            res = db.query(AppList).filter(
                or_(
                    AppList.busniess_name.like('%'+query+'%'),
                    AppList.app_name.like('%'+query+'%'),
                    AppList.app_cluster.like('%'+query+'%'),
                    AppList.app_ip.like('%'+query+'%'),
                    AppList.app_nameid.like('%'+query+'%'),
                    AppList.app_pgm.like('%'+query+'%')
                )
            ).limit(page_size).offset(page_size*(page_index-1))
        except Exception as e:
            response_info['meta'] = {'msg': str(e), 'status': 400 }
            return response_info
    elif query_tag == 2 and query != '':
        try:
            count = db.query(func.count(AppList.id)).filter(
                or_(
                    AppList.busniess_name == query,
                    AppList.app_name.like == query,
                    AppList.app_cluster == query,
                    AppList.app_ip == query,
                    AppList.app_nameid == query,
                    AppList.app_pgm == query
                )
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
            res = db.query(AppList).filter(
                or_(
                    AppList.busniess_name == query,
                    AppList.app_name.like == query,
                    AppList.app_cluster == query,
                    AppList.app_ip == query,
                    AppList.app_nameid == query,
                    AppList.app_pgm == query
                )
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
        temp['id']            = i.id
        temp['busniess_name'] = i.busniess_name
        temp['app_name']      = i.app_name
        temp['app_cluster']   = i.app_cluster
        temp['app_ip']        = i.app_ip
        temp['data_src']      = i.data_src
        temp['app_nameid']    = i.app_nameid
        temp['app_pgm']       = i.app_pgm
        app_list.append(temp)
    response_info['data'] = { 'total_page': total_page,
                              'total_rows': count,
                              'page_index': page_index,
                              'app_list': app_list }
    return response_info


@router.post('/add_applist')
async def add_applist(app_info: AddAppList, db: Session = Depends(create_session), username=Depends(auth_handler.auth_wrapper)):
    response_info = { 'data': {},
                      'meta': { 'msg': 'Add success', 
                                'status': 200 } }
    res  = db.query(AppList).filter(
               and_(
                    AppList.app_name    == app_info.app_nameid,
                    AppList.app_cluster == app_info.app_cluster,
                    AppList.app_ip      == app_info.app_ip
                    )).all()
    if len(res) != 0:
        response_info['meta'] = { 'msg': 'Appinfo already exists!', 'status': 401 }
        return response_info
    if app_info.app_nameid:
        t_app_nameid = app_info.app_nameid
    else:
        import uuid
        random_id = uuid.uuid1()
        random_id = str(random_id).split('-')[0:-1]
        t_app_nameid = ''.join(random_id)
    new_app = AppList(
                      busniess_name = app_info.busniess_name,
                      app_name = app_info.app_name,
                      app_cluster = app_info.app_cluster,
                      app_ip = app_info.app_ip,
                      app_nameid = t_app_nameid,
                      app_pgm = app_info.app_pgm,
                      data_src = 'manul'
                     )
    try:
        db.add(new_app)
        db.commit()
    except Exception as e:
        response_info['meta'] = { 'msg': str(e), 'status': 400 }
        return response_info
    return response_info


@router.put('/mod_applist')
async def mod_applist(app_info: ModAppList, db: Session = Depends(create_session), username=Depends(auth_handler.auth_wrapper)):
    response_info = { 'data': {},
                      'meta': { 'msg': 'Mod success', 
                                'status': 200 }}
    res  = db.query(AppList).filter(and_(
                                         AppList.app_name    == app_info.app_name,
                                         AppList.app_cluster == app_info.app_cluster,
                                         AppList.app_ip      == app_info.app_ip
                                        )
                                    ).all()
    if len(res) != 0:
        response_info['meta'] = { 'msg': 'Appinfo already exists!', 'status': 401 }
        return response_info
    new_app = { 'busniess_name': app_info.busniess_name,
                'app_name': app_info.app_name,
                'app_cluster': app_info.app_cluster,
                'app_ip': app_info.app_ip,
                'app_pgm': app_info.app_pgm }
    try:
        db.query(AppList).filter(AppList.id == app_info.app_id).update(new_app)
        db.commit()
    except Exception as e:
        response_info['meta'] = { 'msg': str(e), 'status': 400 }
        return response_info
    return response_info

@router.delete('/delete_applist')
async def delete_applist(id: int, 
                     db: Session = Depends(create_session), 
                     username=Depends(auth_handler.auth_wrapper)):
    response_info = { 
                        'data': {},
                        'meta': { 'msg': 'Delete success', 'status': 200 }
                    }
    res  = db.query(AppList).filter(AppList.id == id).all()
    if len(res) == 0:
        response_info['meta'] = {'msg': 'Already delete!', 'status': 401 }
        return response_info
    try:
        db.query(AppList).filter(AppList.id == id).delete()
        db.commit()
    except Exception as e:
        response_info['meta'] = { 'msg': str(e), 'status': 400 }
        return response_info
    return response_info