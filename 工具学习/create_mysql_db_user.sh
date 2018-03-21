#!bin/bash
#参考文档：http://blog.csdn.net/wyl9527/article/details/72655277

HOST="localhost"
PORT="3306"
USERNAME="root"
PASSWORD="123456"
DBNAME=$1


connect_cmd="mysql -h${HOST} -P${PORT} -u${USERNAME} -p${PASSWORD}"
${connect_cmd} << EOF

DROP DATABASE IF EXISTS $DBNAME;
CREATE DATABASE $DBNAME CHARACTER SET utf8;
CREATE USER IF NOT EXISTS ${DBNAME}@'%' IDENTIFIED BY 'qwerasdf';
GRANT ALL ON ${DBNAME}.* TO '${DBNAME}'@'%';
FLUSH PRIVILEGES;

EOF

[ $? -eq 0 ] && echo "Create database and user ${DBNAME} success. password is 'qwerasdf'"
