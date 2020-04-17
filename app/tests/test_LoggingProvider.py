from app.Providers.LoggingProvider import LoggingProvider
import logging
from testfixtures import LogCapture


class TestGetLogger:

    def test_can_get_new_logger(self, test_logging_provider):
        logger = test_logging_provider._get_logger("test_name")
        assert test_logging_provider.loggers == {"test_name": logger}

    def test_can_get_existing_logger(self):
        logging_provider = LoggingProvider()
        test_logger = logging.getLogger()
        logging_provider.loggers.update({"test_name": test_logger})
        retrieved_logger = logging_provider._get_logger("test_name")
        assert logging_provider.loggers == {"test_name": test_logger}
        assert retrieved_logger == test_logger


class TestLogging:

    def test_can_log_info(self, test_logging_provider):
        with LogCapture() as log_capture:
            test_logging_provider.info("test_name", "test message")
            log_capture.check(
                ("test_name", 'INFO', 'test message')
            )

    def test_can_log_warning(self, test_logging_provider):
        with LogCapture() as log_capture:
            test_logging_provider.warning("test_name", "test message")
            log_capture.check(
                ("test_name", 'WARNING', 'test message')
            )

    def test_can_log_error(self, test_logging_provider):
        with LogCapture() as log_capture:
            test_logging_provider.error("test_name", "test message")
            log_capture.check(
                ("test_name", 'ERROR', 'test message')
            )

    def test_can_log_debug(self, test_logging_provider):
        with LogCapture() as log_capture:
            test_logging_provider.debug("test_name", "test message")
            log_capture.check(
                ("test_name", 'DEBUG', 'test message')
            )
