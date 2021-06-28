FROM tiangolo/uvicorn-gunicorn:python3.8-slim
#ENV LANG en_US.UTF-8
#RUN apk add -U tzdata \
#    && cp -r -f /usr/share/zoneinfo/Hongkong /etc/localtime


#RUN pip install --no-cache-dir fastapi sqlalchemy uvicorn passlib bcrypt pyjwt aiofiles -i https://pypi.tuna.tsinghua.edu.cn/simple/
#RUN pip install --no-cache-dir PyMySql fastapi sqlalchemy uvicorn passlib[bcrypt] pyjwt aiofiles -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
RUN pip install --no-cache-dir PyMySql fastapi sqlalchemy uvicorn passlib[bcrypt] pyjwt aiofiles

#COPY ./app /app

ENV app /app/
WORKDIR ${app}
ADD app.tar $app

EXPOSE 5000
CMD ["python3", "main.py"]
