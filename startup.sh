#!/bin/bash

service nginx restart
NEW_RELIC_CONFIG_FILE=/var/www/app/config/newrelic.ini newrelic-admin run-program python /var/www/app/run.py -c /var/www/app/config/config.json
