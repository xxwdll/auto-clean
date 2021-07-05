from fastapi import APIRouter
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.sql.expression import null
from lib.auth import AuthHandler
from lib.schemas import AuthDetails
from lib.models import AlarmInfo, App, Script
from lib.database import create_session
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.sql import and_, or_
from datetime import datetime,timedelta
import calendar


router = APIRouter()
auth_handler = AuthHandler()

def cal_times(spendtime):
    days      = round(spendtime/(3600*24))
    spendtime = spendtime%(3600*24)
    hours     = round(spendtime/3600)
    spendtime = spendtime%3600
    minutes   = round(spendtime/60)
    seconds   = spendtime%60
    spendtime = ''
    if days != 0:
        spendtime += str(days) + '天'
    if hours != 0:
        spendtime += str(hours) + '时'
    if minutes != 0:
        spendtime += str(minutes) + '分'
    if seconds != 0:
        spendtime += str(seconds) + '秒'
    return spendtime


def cal_space(cleanspace):
    GB = round(cleanspace/1024/1024)
    cleanspace = cleanspace%(1024*1024)
    MB = round(cleanspace/1024)
    cleanspace = ''
    if GB != 0:
        cleanspace += str(GB) + 'G '
    if MB != 0:
        cleanspace += str(MB) + 'M'
    return cleanspace


@router.get('/home_head')
async def get_home_head(username=Depends(auth_handler.auth_wrapper),
                        db: Session = Depends(create_session)):
    response_info = { 'data': {},
                      'meta': { 'msg': 'Get HeadInfo success', 
                                'status': 200 }}
    try:
        cleantimes = db.query(func.count(AlarmInfo.id)).scalar()
        spendtime  = db.query(func.sum(AlarmInfo.spend_time)).scalar()
        cleanspace = db.query(func.sum(AlarmInfo.clean_space)).scalar()
        res        = db.query(App.ip
                         ).join(Script, Script.cluster_name==App.cluster_info
                         ).filter(App.ip.like('%.%')
                         ).with_entities(App.ip).distinct().all()
        machines  = len(res)
    except Exception as e:
        response_info['meta'] = {'msg': str(e), 'status': 400 }
        return response_info
    spendtime = cal_times(spendtime)
    cleanspace = cal_space(cleanspace)
    response_info['data'] = {
                                'spendtime': spendtime,
                                'cleanspace': cleanspace,
                                'cleantimes': cleantimes,
                                'machines': machines
                            }
    return response_info


@router.get('/home_top_list')
async def get_home_top_list(username=Depends(auth_handler.auth_wrapper),
                            db: Session = Depends(create_session)):
    response_info = { 'data': {},
                      'meta': { 'msg': 'Get TopList success', 
                                'status': 200 }}
    now_time   = datetime.utcnow() + timedelta(hours=8)
    now_month  = '%' + str(now_time.strftime("%Y-%m")) + '%'
    try:
        #res = db.query(AlarmInfo).limit(10).all()
        count = func.count(AlarmInfo.ip).label('count')
        res = db.query(AlarmInfo.ip,
                       count,
                       AlarmInfo.path,
                       func.sum(AlarmInfo.clean_space).label('space'))\
                .filter(AlarmInfo.start_time.like(now_month))\
                .group_by(AlarmInfo.ip).order_by(count.desc()).limit(10).all()
    except Exception as e:
        response_info['meta'] = {'msg': str(e), 'status': 400 }
        return response_info
    top_list = []
    for i in res:
        temp = {}
        temp['ip'] = i.ip
        temp['path'] = i.path
        temp['count'] = i.count
        temp['space'] = cal_space(i.space)
        top_list.append(temp)
    response_info['data'] = {
                                'toplist': top_list
                            }
    return response_info


@router.get('/home_charts_month')
async def get_home_charts_month(username=Depends(auth_handler.auth_wrapper),
                                db: Session = Depends(create_session)):
    response_info = { 'data': {},
                      'meta': { 'msg': 'Get charts', 
                                'status': 200 }}
    now_time = datetime.utcnow()
    time = now_time + timedelta(hours=8)
    now_month  = int(time.strftime("%m"))
    now_year   = int(time.strftime("%Y"))
    total_days = calendar.monthrange(now_year, now_month)[1]
    days_count  = []
    if now_month < 10:
        now_month = '0' + str(now_month)
    for i in range(total_days):
        today = i + 1
        if today < 10:
            today = '0' + str(today)
        today = '%' + str(now_year) + '-' + str(now_month) + '-' + str(today) + '%'
        try:
            count = db.query(func.count(AlarmInfo.id))\
                      .filter(AlarmInfo.start_time.like(today))\
                      .scalar()
            days_count.append(count)
        except Exception as e:
            response_info['meta'] = {'msg': str(e), 'status': 400 }
            return response_info
    title = '次数统计 ' + str(now_month) + ' 月'
    xAxis_data  = []
    series_data = []
    today       = 0
    for i in days_count:
        today = today + 1
        xAxis_data.append(str(today) + '日')
        series_data.append(str(i))
    response_info['data'] = {
                                'title': title,
                                'xAxis_data': xAxis_data,
                                'series_data': series_data
                            }
    return response_info