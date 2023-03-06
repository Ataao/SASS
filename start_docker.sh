#!/bin/sh
docker build -t mongodb-container .
docker run -dp 27017:27017 --name mongodb-run mongodb-container bash -c "mongod"
docker cp setup_db.js mongodb-run:/root/
docker exec mongodb-run bash -c "mongosh < /root/setup_db.js"
