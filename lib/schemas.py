from pydantic import BaseModel

class AuthDetails(BaseModel):
    username: str
    password: str

class ResetPass(BaseModel):
    password: str
    newpassword: str

class AddAppInfo(BaseModel):
    ip: str
    cluster_info: str


class ModAppInfo(BaseModel):
    app_id: int
    ip: str
    cluster_info: str


class AddScriptInfo(BaseModel):
    cluster_name: str
    type_info: str
    command: str


class ModScriptInfo(BaseModel):
    auto_key: int
    cluster_name: str
    type_info: str
    command: str


class AddAppList(BaseModel):
    busniess_name: str
    app_name: str
    app_cluster: str
    app_ip: str
    # data_src: str
    app_nameid: str
    app_pgm: str


class ModAppList(BaseModel):
    app_id: int
    busniess_name: str
    app_name: str
    app_cluster: str
    app_ip: str
    app_pgm: str


class AddScriptTemp(BaseModel):
    label: str
    command: str


class ModScriptTemp(BaseModel):
    # value: int
    id: int
    label: str
    command: str


class AddAlarmInfo(BaseModel):
    ip: str
    start_time: int
    end_time: int
    path: str
    clean_space: int
    disk_percent: str
    token: str