#!/bin/sh
docker build -t mongodb-container .
docker run -dp 27017:27017 mongodb-container
docker exec -t mongodb-container "mongosh < setup_db.js"
