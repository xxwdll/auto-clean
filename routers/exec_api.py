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
import math, os


router = APIRouter()
auth_handler = AuthHandler()


@router.get('/update_data')
async def update_data(
                         username=Depends(auth_handler.auth_wrapper)
                      ):
    response_info = { 
                      'data': {},
                      'meta': { 
                                'msg': 'success', 
                                'status': 200
                              }
                    }
    exec_file = os.path.join('lib', 'update_v2.py')
    cmd       = 'python ' + exec_file
    try:
        data = os.popen(cmd).read()
    except Exception as e:
        response_info['meta'] = {
                                    'msg': 'error!==>' + str(e),
                                    'status': 201
                                 }
    else:
        response_info['data'] = data
    return response_info