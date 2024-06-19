#!/bin/bash

mkdir -p /var/log/uwsgi/app/; touch /var/log/uwsgi/app/cdc-service.log

service nginx restart
/usr/local/bin/circusd /var/www/app/config/circus.conf
