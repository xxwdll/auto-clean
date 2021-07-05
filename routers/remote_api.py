from fastapi import APIRouter, Response
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import null
from lib.auth import AuthHandler
from lib.schemas import AuthDetails, AddAlarmInfo
from lib.models import App, Script, AlarmInfo
from lib.database import create_session
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.sql import and_, or_
from datetime import datetime, timezone, timedelta


router = APIRouter()

# 以下为提供外部调用接口， 非web接口

@router.get('/checkip')
async def get_all_need_clean_ip(db: Session = Depends(create_session)):
    res = db.query(App).join(Script, Script.cluster_name==App.cluster_info).filter(App.ip.like('%.%')).with_entities(App.ip).distinct().all()
    ips = ''
    for i in res:
        ips = ips + str(i['ip']) + '\n'
    return Response(content=ips.rstrip("\n"))


# scriptinfo?ip=$t_ip&path=$this_path
@router.get('/scriptinfo')
async def get_script_by_path_ip(ip: str,
                                path: str,
                                db: Session = Depends(create_session)):
    res = db.query(App.cluster_info).filter(App.ip==ip).distinct().all()
    cluster_infos = []
    [ cluster_infos.append(i['cluster_info']) for i in res ]
    res = db.query(Script.command).filter(and_(
        Script.type_info==path,
        Script.cluster_name.in_(cluster_infos)
    )).distinct().all()
    print(res)
    command = ''
    if len(res) == 0:
        temp_res = db.query(Script.command).filter(and_(
                       Script.type_info=='null',
                       Script.cluster_name=='null_script_temp'
                   )).distinct().first()
        command = "root_dir=" + path + '\n' + temp_res[0]
    for i in res:
        command = command + str(i['command']) + '\n'
    return Response(content=command)

# typeinfo/$t_ip
@router.get('/typeinfo/{ip}')
async def get_scriptinfo_by_ip(ip, db: Session = Depends(create_session),):
    res = db.query(App.cluster_info).filter(App.ip==ip).distinct().all()
    cluster_infos = []
    [ cluster_infos.append(i['cluster_info']) for i in res ]
    res = db.query(Script.type_info).filter(Script.cluster_name.in_(cluster_infos)).distinct().all()
    paths = ''
    for i in res:
        paths = paths + str(i['type_info']) + ';;'
    return Response(content=paths)

@router.post('/add_alarm_info')
async def add_alarm_info(_info: AddAlarmInfo,
                         db: Session = Depends(create_session)):
    response_info = 'success'
    tz            = timezone(timedelta(hours=+8))
    start_time    = datetime.fromtimestamp(_info.start_time, tz=tz)
    end_time      = datetime.fromtimestamp(_info.end_time, tz=tz)
    if _info.clean_space == 0:
        response_info = 'useless!'
        return Response(content=response_info)
    if _info.token != 'auysgdsahdjas9':
        response_info = 'token error!'
        return Response(content=response_info)
    res = db.query(AlarmInfo).filter(
                                     and_(
                                          AlarmInfo.start_time == start_time,
                                          AlarmInfo.ip == _info.ip
                                     )
                            ).all()
    if len(res) != 0:
        response_info = 'already exists!'
        return Response(content=response_info)
    new_data = AlarmInfo(
                         ip = _info.ip,
                         start_time = start_time,
                         end_time = end_time,
                         spend_time = _info.end_time - _info.start_time,
                         path = _info.path,
                         clean_space = _info.clean_space,
                         disk_percent = _info.disk_percent
               )
    try:
        db.add(new_data)
        db.commit()
    except Exception as e:
        response_info = str(e)
    return Response(content=response_info)
