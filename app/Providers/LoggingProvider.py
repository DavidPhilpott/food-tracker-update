import logging
import os


class LoggingProvider:
    def __init__(self):
        self.loggers = {}

        self.log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        if "LOG_FORMAT" in os.environ:
            self.format = os.environ["LOG_FORMAT"]

        self.log_level = "DEBUG"
        if "LOG_LEVEL" in os.environ:
            self.level = os.environ["LOG_LEVEL"]

    def _get_logger(self, name):
        
