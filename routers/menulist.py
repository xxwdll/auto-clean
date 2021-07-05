from fastapi import APIRouter
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.sql.expression import null
from lib.auth import AuthHandler
from lib.schemas import AuthDetails, AddAppInfo, ModAppInfo
from lib.models import User, App, Menu, Script
from lib.database import create_session
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.sql import and_, or_
import math


router = APIRouter()
auth_handler = AuthHandler()


@router.get('/api/menus', tags=['menulist'])
async def get_menus(username=Depends(auth_handler.auth_wrapper), db: Session = Depends(create_session)):
    data = []
    meta = {}
    menus = db.query(Menu).filter(Menu.menu_level==1).all()
    if (menus is None):
        #raise HTTPException(status_code=401, detail='Invalid username and/or password')
        meta['msg']    = 'Menus is None'
        meta['status'] = 404
        return { 'data': data, 'meta': meta }
    for i in menus:
        menu_item     = {}
        menu_item['id'] = i.menu_id
        menu_item['authName'] = i.menu_name
        menu_item['path'] = i.menu_path
        menu_item['children'] = []
        chilren_menus = db.query(Menu).filter(Menu.father_id==i.menu_id).all()
        if chilren_menus == None:
            data.append(menu_item)
            continue
        for j in chilren_menus:
            children_menu_item             = {}
            children_menu_item['id']       = j.menu_id
            children_menu_item['authName'] = j.menu_name
            children_menu_item['path']     = j.menu_path
            children_menu_item['children'] = []
            menu_item['children'].append(children_menu_item)
        data.append(menu_item)
    meta['msg']      = 'Get menu list success'
    meta['status']   = 200
    return { 'data': data, 'meta': meta }
