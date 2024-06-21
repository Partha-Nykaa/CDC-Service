import logging

from main.common.nykaa_logger import CustomJsonFormatter
from main.common.singleton import Singleton

ACTIVITY = "activity"
APPLICATION = "application"


@Singleton
class RootLoggerFactory:
    @staticmethod
    def get_logger(name: str = None):
        return logging.getLogger(f"{name}")

    @staticmethod
    def setup():
        fmt = '%(timestamp) %(level) %(name) %(lineno) %(message)'
        fh = logging.FileHandler("logs/nykaa_catalog.json")
        fh.setFormatter(CustomJsonFormatter(fmt))
        logging.basicConfig(level=logging.INFO, handlers=[fh])


@Singleton
class ApplicationLoggerFactory:
    @staticmethod
    def get_logger(name: str = None):
        logger_name = APPLICATION
        if name:
            logger_name = f"{APPLICATION}.{name}"
        return logging.getLogger(logger_name)

    @staticmethod
    def setup(logger=None):
        fmt = '%(timestamp) %(level) %(name) %(lineno) %(message)'
        handler = logging.FileHandler("logs/nykaa_catalog.json")
        handler.setFormatter(CustomJsonFormatter(fmt))
        logger = logger if logger else logging.getLogger(APPLICATION)
        logger.setLevel(logging.INFO)
        logger.propagate = False
        logger.addHandler(handler)


@Singleton
class ActivityLoggerFactory:
    @staticmethod
    def get_logger(name: str = None):
        logger_name = ACTIVITY
        if name:
            logger_name = f"{ACTIVITY}.{name}"
        return logging.getLogger(logger_name)

    @staticmethod
    def setup(logger=None):
        fmt = '%(timestamp) %(level) %(method) %(path) %(status) %(name) %(lineno) %(message)'
        handler = logging.FileHandler("logs/nykaa_catalog_activity.json")
        handler.setFormatter(CustomJsonFormatter(fmt))
        logger = logger if logger else logging.getLogger(ACTIVITY)
        logger.setLevel(logging.INFO)
        logger.propagate = False
        logger.addHandler(handler)
