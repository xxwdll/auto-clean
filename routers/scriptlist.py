from fastapi import APIRouter
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.sql.expression import null
from lib.auth import AuthHandler
from lib.schemas import AuthDetails, AddScriptInfo, ModScriptInfo
from lib.models import Script, ScriptTemp
from lib.database import create_session
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.sql import and_, or_
import math


router = APIRouter()
auth_handler = AuthHandler()


@router.get('/query_script')
async def get_script_list(page_index: int,
                          page_size: int,
                          query: str,
                          query_tag: int,
                          db: Session = Depends(create_session),
                          username=Depends(auth_handler.auth_wrapper)):
    response_info = { 'data': {},
                      'meta': { 'msg': 'Get script list success', 
                                'status': 200 }}
    if query_tag == 0 or query == '' or query_tag == 3:
        try:                                
            count      = db.query(func.count(Script.auto_key)).scalar()
            total_page = math.ceil(count/page_size)
        except Exception as e:
            response_info['meta'] = {'msg': str(e), 'status': 400 }
            return response_info
        if query_tag == 3 or page_index > total_page:
            page_index = total_page
        try:
            res = db.query(Script).limit(page_size).offset(page_size*(page_index-1))
        except Exception as e:
            response_info['meta'] = {'msg': str(e), 'status': 400 }
            return response_info
    elif query_tag == 1 and query != '':
        try:
            count = db.query(func.count(Script.auto_key)).filter(
                        or_(Script.cluster_name.like('%'+query+'%'),
                            Script.type_info.like('%'+query+'%'),
                            Script.command.like('%'+query+'%'))
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
            res = db.query(Script).filter(
                or_(Script.cluster_name.like('%'+query+'%'),
                    Script.type_info.like('%'+query+'%'),
                    Script.command.like('%'+query+'%'))
            ).limit(page_size).offset(page_size*(page_index-1))
        except Exception as e:
            response_info['meta'] = {'msg': str(e), 'status': 400 }
            return response_info
    elif query_tag == 2 and query != '':
        try:
            count = db.query(func.count(Script.auto_key)).filter(
                or_(Script.cluster_name == query,
                    Script.type_info == query,
                    Script.command == query)
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
            res = db.query(Script).filter(
                or_(Script.cluster_name == query,
                    Script.type_info == query,
                    Script.command == query)
            ).limit(page_size).offset(page_size*(page_index-1))
        except Exception as e:
            response_info['meta'] = {'msg': str(e), 'status': 400 }
            return response_info
    else:
        response_info['meta'] = { 'msg': 'Method not found!', 'status': 404 }
        return response_info
    app_list = []
    for i in res:
        temp = {}
        temp['cluster_name'] = i.cluster_name
        temp['type_info']    = i.type_info
        temp['command']      = i.command
        temp['auto_key']     = i.auto_key
        app_list.append(temp)
    response_info['data'] = { 'total_page': total_page,
                              'total_rows': count,
                              'page_index': page_index,
                              'app_list': app_list }
    return response_info


@router.post('/add_script')
async def add_script(script_info: AddScriptInfo,
                     db: Session = Depends(create_session),
                     username = Depends(auth_handler.auth_wrapper)):
    response_info = { 'data': {},
                      'meta': { 'msg': 'Add success',
                                'status': 200 } }
    cluster_name = script_info.cluster_name
    type_info    = script_info.type_info
    command      = script_info.command
    res = db.query(Script).filter(
              and_(Script.cluster_name == cluster_name,
              Script.type_info == type_info,
              Script.command == command)).all()
    if len(res) != 0:
        response_info['meta'] = { 'msg': 'Scriptinfo already exists!', 'status': 401 }
        return response_info
    new_data = Script(cluster_name = script_info.cluster_name,
                      type_info = script_info.type_info,
                      command = script_info.command)
    try:
        db.add(new_data)
        db.commit()
    except Exception as e:
        response_info['meta'] = { 'msg': str(e), 'status': 400 }
        return response_info
    return response_info


@router.put('/mod_script', tags=['applist'])
async def mod_script(script_info: ModScriptInfo,
                     db: Session = Depends(create_session),
                     username = Depends(auth_handler.auth_wrapper)):
    response_info = { 'data': {},
                      'meta': { 'msg': 'Mod success', 
                                'status': 200 }}
    cluster_name = script_info.cluster_name
    type_info    = script_info.type_info
    command      = script_info.command
    auto_key     = script_info.auto_key
    res  = db.query(Script).filter(
              and_(Script.cluster_name == cluster_name,
              Script.type_info == type_info,
              Script.command == command)).all()
    if len(res) != 0:
        response_info['meta'] = { 'msg': 'Repeat data!', 'status': 401 }
        return response_info
    new_app = { 'cluster_name': cluster_name,
                'type_info': type_info,
                'command': command }
    try:
        db.query(Script).filter(Script.auto_key == auto_key).update(new_app)
        db.commit()
    except Exception as e:
        response_info['meta'] = { 'msg': str(e), 'status': 400 }
        return response_info
    return response_info


@router.delete('/delete_script')
async def delete_script(auto_key: int, 
                     db: Session = Depends(create_session), 
                     username=Depends(auth_handler.auth_wrapper)):
    response_info = { 
                        'data': {},
                        'meta': { 'msg': 'Delete success', 'status': 200 }
                    }
    res  = db.query(Script).filter(Script.auto_key == auto_key).all()
    if len(res) == 0:
        response_info['meta'] = {'msg': 'Already delete or not found!', 'status': 401 }
        return response_info
    try:
        db.query(Script).filter(Script.auto_key == auto_key).delete()
        db.commit()
    except Exception as e:
        response_info['meta'] = { 'msg': str(e), 'status': 400 }
        return response_info
    return response_info
