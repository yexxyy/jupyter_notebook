#!/bin/bash

#$1 -> db name
#$2 -> user name

if [ -z $1 ] || [ -z $2 ];then
    echo "Pleace input both db name and user name."
    exit 2
fi
    
HOST="localhost"
PORT="3306"
USERNAME="root"
PASSWORD="123456"
TEMP_DB=$1
TEMP_USER=$2
TEMP_PASSWORD=`openssl rand -hex 4`

connect_cmd="mysql -h${HOST} -P${PORT} -u${USERNAME} -p${PASSWORD}"
${connect_cmd} << EOF

CREATE DATABASE $TEMP_DB CHARACTER SET UTF8;
CREATE USER IF NOT EXISTS ${TEMP_USER}@'%' IDENTIFIED BY '${TEMP_PASSWORD}';
GRANT ALL ON ${TEMP_DB}.* TO '${TEMP_USER}'@'%';
FLUSH PRIVILEGES;

EOF

[ $? -eq 0 ] && echo "Create database ${TEMP_DB} and user ${TEMP_USER} success. Password is ${TEMP_PASSWORD}"

