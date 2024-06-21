import threading
from datetime import datetime

from flask import session, has_request_context
from pythonjsonlogger import jsonlogger

from main.common import CommonConstant
from main.common.session_provider import SessionProvider


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
            log_record['timestamp'] = now

        if has_request_context():
            log_record['request_id'] = session.get(CommonConstant.request_id, "")
        elif "request_id" in threading.current_thread()._kwargs:
            log_record['request_id'] = SessionProvider().session().get(CommonConstant.request_id, "")
        else:
            log_record['request_id'] = "None"

        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname
