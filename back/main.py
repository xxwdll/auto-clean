from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from fastapi.staticfiles import StaticFiles
# Use this to serve a dist/index.html
from starlette.responses import FileResponse 
from starlette.responses import PlainTextResponse
from fastapi.middleware.gzip import GZipMiddleware


from routers import applist, userlist, menulist,\
                    scriptlist, newapplist, scripttemp,\
                    remote_api, exec_api


app = FastAPI()
app.include_router(applist.router)
app.include_router(userlist.router)
app.include_router(menulist.router)
app.include_router(scriptlist.router,
                   prefix="/api",
                   tags=['scriptlist'])
app.include_router(newapplist.router,
                   prefix="/api",
                   tags=['app_list'])
app.include_router(scripttemp.router,
                   prefix="/api",
                   tags=['script_temp'])
app.include_router(remote_api.router,
                   prefix="/remote_api",
                   tags=['remote_api'])
app.include_router(exec_api.router,
                   prefix="/api/exec_api",
                   tags=['exec_api'])
app.mount("/static", StaticFiles(directory="dist/static"), name="static")
app.add_middleware(GZipMiddleware, minimum_size=1000)


# 前端页面url
origins = ['*']
# 后台api允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def read_index():
    return FileResponse('dist/index.html')


def main():
    import uvicorn
    uvicorn.run(
                    app="main:app", 
                    #host="127.0.0.1", 
                    host="0.0.0.0", 
                    port=5000,
                    reload=True, 
                    debug=True, 
                    log_level="info"
                )


if __name__ == '__main__':
    main()
