#!/bin/bash

IP="34.90.88.125"
sed -i "s/IP/$IP/g" /var/www/html/index.html
echo $IP > /var/www/html/ip

cd /app/mail/
python3 /app/mail/app.py &
cd /app/auth/
python3 /app/auth/app.py &
cd /
/usr/sbin/nginx -g "daemon off;"
