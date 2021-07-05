from fastapi import APIRouter
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.sql.expression import label, null
from sqlalchemy.sql.operators import comma_op
from lib.auth import AuthHandler
from lib.schemas import AuthDetails, AddScriptTemp, ModScriptTemp
from lib.models import ScriptTemp
from lib.database import create_session
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.sql import and_, or_
import math


router = APIRouter()
auth_handler = AuthHandler()


@router.get('/query_script_temp')
async def get_script_temp(page_index: int,
                          page_size: int,
                          query: str,
                          query_tag: int,
                          db: Session = Depends(create_session),
                          username=Depends(auth_handler.auth_wrapper)):
    response_info = { 'data': {},
                      'meta': { 'msg': 'Get ScriptTemp list success', 
                                'status': 200 }}                       
    if query_tag == 0 or query == '' or query_tag == 3:
        try:                                
            count      = db.query(func.count(ScriptTemp.id)).scalar()
            total_page = math.ceil(count/page_size)
        except Exception as e:
            response_info['meta'] = {'msg': str(e), 'status': 400 }
            return response_info
        if query_tag == 3 or page_index > total_page:
            page_index = total_page
        try:
            res = db.query(ScriptTemp).limit(page_size).offset(page_size*(page_index-1))
        except Exception as e:
            response_info['meta'] = {'msg': str(e), 'status': 400 }
            return response_info
    elif query_tag == 1 and query != '':
        try:
            count = db.query(func.count(ScriptTemp.id)).filter(
                        or_(
                            ScriptTemp.command.like('%'+query+'%'),
                            ScriptTemp.label.like('%'+query+'%')
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
            res = db.query(ScriptTemp).filter(
                      or_(
                          ScriptTemp.command.like('%'+query+'%'),
                          ScriptTemp.label.like('%'+query+'%')
                      )
                  ).limit(page_size).offset(page_size*(page_index-1))
        except Exception as e:
            response_info['meta'] = {'msg': str(e), 'status': 400 }
            return response_info
    elif query_tag == 2 and query != '':
        try:
            count = db.query(func.count(ScriptTemp.id)).filter(
                        or_(
                            ScriptTemp.label == query,
                            ScriptTemp.command == query
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
            res = db.query(ScriptTemp).filter(
                      or_(
                          ScriptTemp.label == query,
                          ScriptTemp.command == query
                      )
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
        temp['id']      = i.id
        temp['label']   = i.label
        temp['command'] = i.command
        app_list.append(temp)
    response_info['data'] = { 'total_page': total_page,
                              'total_rows': count,
                              'page_index': page_index,
                              'app_list': app_list }
    return response_info


@router.post('/add_script_temp')
async def add_script_temp(_info: AddScriptTemp,
                           db: Session = Depends(create_session),
                           username = Depends(auth_handler.auth_wrapper)):
    response_info = { 'data': {},
                      'meta': { 'msg': 'Add success',
                                'status': 200 } }
    label   = _info.label
    command = _info.command
    res = db.query(ScriptTemp).filter(
              and_(
                  ScriptTemp.label == label,
                  ScriptTemp.command == command
              )
          ).all()
    if len(res) != 0:
        response_info['meta'] = { 'msg': 'ScriptTempinfo already exists!', 'status': 401 }
        return response_info
    new_data = ScriptTemp(
                          label = _info.label,
                          command = _info.command
               )
    try:
        db.add(new_data)
        db.commit()
    except Exception as e:
        response_info['meta'] = { 'msg': str(e), 'status': 400 }
        return response_info
    return response_info


@router.put('/mod_script_temp')
async def mod_script_temp(_info: ModScriptTemp,
                          db: Session = Depends(create_session),
                          username = Depends(auth_handler.auth_wrapper)
                         ):
    response_info = { 'data': {},
                      'meta': { 'msg': 'Mod success', 
                                'status': 200 }}
    id      = _info.id
    label   = _info.label
    command = _info.command
    res  = db.query(ScriptTemp).filter(
               and_(
                    ScriptTemp.label   == label,
                    ScriptTemp.command == command
                   )
           ).all()
    if len(res) != 0:
        response_info['meta'] = { 'msg': 'Repeat data!', 'status': 401 }
        return response_info
    new_app = { 
                  'label': label,
                  'command': command
              }
    try:
        db.query(ScriptTemp).filter(ScriptTemp.id == id).update(new_app)
        db.commit()
    except Exception as e:
        response_info['meta'] = { 'msg': str(e), 'status': 400 }
        return response_info
    return response_info


@router.delete('/delete_script_temp')
async def delete_script_temp(id: int, 
                             db: Session = Depends(create_session), 
                             username=Depends(auth_handler.auth_wrapper)):
    response_info = { 
                        'data': {},
                        'meta': { 'msg': 'Delete success', 'status': 200 }
                    }
    res  = db.query(ScriptTemp).filter(ScriptTemp.id == id).all()
    if len(res) == 0:
        response_info['meta'] = {'msg': 'Already delete or not found!', 'status': 401 }
        return response_info
    try:
        db.query(ScriptTemp).filter(ScriptTemp.id == id).delete()
        db.commit()
    except Exception as e:
        response_info['meta'] = { 'msg': str(e), 'status': 400 }
        return response_info
    return response_info


@router.get('/get_all_script_temp')
async def get_all_script_temp(
                              db: Session = Depends(create_session),
                              username=Depends(auth_handler.auth_wrapper)
                             ):
    response_info = { 'data': {},
                      'meta': { 'msg': 'Get ScriptTemp list success', 
                                'status': 200 }}                       
    try:
        res = db.query(ScriptTemp).all()
    except Exception as e:
        response_info['meta'] = {'msg': str(e), 'status': 400 }
        return response_info
    option_list = []
    for i in res:
        temp = {}
        temp['value']      = i.id
        temp['label']   = i.label
        temp['command'] = i.command
        option_list.append(temp)
    response_info['data'] = { 'option_list': option_list }
    return response_info