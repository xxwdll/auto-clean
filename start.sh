docker run -d --name fastapi \
           --log-opt max-size=10m --log-opt max-file=1 \
           -v $PWD/app:/app \
           -p 5000:5000 fastapi:autov2
