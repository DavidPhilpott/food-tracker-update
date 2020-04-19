import logging
import os


class LoggingProvider:
    def __init__(self):
        self.loggers = {}

        self.log_format = logging.Formatter(fmt='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
                                            datefmt='%d-%b-%y %H:%M:%S')
        if "LOG_FORMAT" in os.environ:
            self.log_format = logging.Formatter(fmt=os.environ["LOG_FORMAT"])

        self.log_level = "DEBUG"
        if "LOG_LEVEL" in os.environ:
            self.log_level = os.environ["LOG_LEVEL"]

        # Remove handlers on root logger during startup - removes AWS handler causing duplication
        root = logging.getLogger()
        if root.handlers:
            for handler in root.handlers:
                root.removeHandler(handler)

    def _set_logging_handler(self):
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(self.log_format)
        return log_handler

    def _get_logger(self, name):
        if name not in self.loggers:
            logger = logging.getLogger(name)
            if len(logger.handlers) == 0:
                logger.addHandler(self._set_logging_handler())
            logger.setLevel(self.log_level)
            self.loggers.update({name: logger})
        return self.loggers[name]

    def info(self, name, message):
        logger = self._get_logger(name)
        logger.info(message)

    def warning(self, name, message):
        logger = self._get_logger(name)
        logger.warning(message)

    def debug(self, name, message):
        logger = self._get_logger(name)
        logger.debug(message)

    def error(self, name, message):
        logger = self._get_logger(name)
        logger.error(message)
