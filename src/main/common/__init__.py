from . import singleton

__all__ = ['singleton']

singleton = singleton


class CommonConstant:
    request_id = 'request_id'
    user_id = 'user_id'
    request_start_time = 'request_start_time'
    request_level_cache = 'request_level_cache'
    listing_remarks_collector = 'listing_remarks_collector'
    timer = 'timer'