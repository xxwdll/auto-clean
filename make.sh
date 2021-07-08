
[ ! -d auo-clean ] && mkdir auo-clean

cd auo-clean

start_time=`date +%s`

curl -o Dockerfile -s "https://gitee.com/w_dll/auto-clean/raw/master/Dockerfile"
docker build -t autoclean:$start_time .
[ $? -ne 0 ] && echo 'docker build error!' && exit 1

echo 'docker build done!'

if [ ! -f 'app/lib/auto-clean.db' ];then
  git clone https://gitee.com/w_dll/auto-clean.git app
fi
[ $? -ne 0 ] && echo 'git pull error!' && exit 1

docker run -d --name auo-clean \
           --log-opt max-size=10m --log-opt max-file=1 \
           -v $PWD/app:/app \
           -p 5000:5000 autoclean:$start_time
[ $? -ne 0 ] && echo 'docker run error!' && exit 1

echo 'done! check port 5000!'
