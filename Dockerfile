FROM python:3.8-alpine3.10

LABEL maintainer="wdll <gqoyvf@163.com>"

RUN apk add --no-cache git python3-dev openssl-dev libffi-dev gcc g++ musl-dev && \
    pip install --no-cache-dir PyMySql fastapi sqlalchemy \
                   uvicorn passlib[bcrypt] pyjwt aiofiles \
                -i https://pypi.douban.com/simple/   

ENV app /app/
WORKDIR ${app}
RUN git clone https://gitee.com/w_dll/auto-clean.git ${app}

EXPOSE 5000
CMD ["python3", "main.py"]
