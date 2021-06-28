1. ## fastapi vue demo

   #### 前端
   - 对应文件夹 front

   - vue element ui

   #### 后端
   - 对应文件夹 back

   - python3.8 fastapi
   - 需要的第三方库

   ```cmd
   pip install --no-cache-dir PyMySql fastapi sqlalchemy uvicorn passlib[bcrypt] pyjwt aiofiles
   ```

   #### 环境
   redhat6 内核太低，用docker也测试失败
   centos7; windows 7,10; 测试成功

   #### 测试
   python main.py
   运行后 测试地址为 http://localhost:5000
   用户名 admin
   密码 123456