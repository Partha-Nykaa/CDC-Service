import threading

from flask import session

from main.common import CommonConstant


# TODO find a library for this
class SessionProvider:
    def __init__(self):
        self.__session = session

        thread_stack = threading.current_thread()._kwargs
        if "request_id" in thread_stack:
            self.__session = thread_stack

    @staticmethod
    def create_session_non_flask(request_id, user_id, roles=[]):
        thread_stack = threading.current_thread()._kwargs
        thread_stack.update({
            "request_id": request_id,
            "user_id": user_id,
            "roles": roles,
        })

    def session(self):
        return self.__session

    def delete_session_non_flask(self):
        sess = self.session()
        sess.pop('request_level_cache', None)
        sess.pop("listing_remarks_collector", None)

    def get_request_id(self):
        return str(self.__session.get(CommonConstant.request_id, ""))
