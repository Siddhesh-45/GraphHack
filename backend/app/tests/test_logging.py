import json
import logging
from app.core.logging import JSONFormatter, setup_logging, get_logger

def test_json_formatter_structure():
    formatter = JSONFormatter()
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test.py",
        lineno=10,
        msg="Test logging message",
        args=(),
        exc_info=None
    )
    formatted = formatter.format(record)
    parsed = json.loads(formatted)
    assert parsed["level"] == "INFO"
    assert parsed["name"] == "test_logger"
    assert parsed["message"] == "Test logging message"
    assert "timestamp" in parsed
    assert "environment" in parsed

def test_get_logger():
    logger = get_logger("my_test_component")
    assert logger.name == "my_test_component"

def test_setup_logging_idempotent():
    setup_logging()
    root_logger = logging.getLogger()
    assert len(root_logger.handlers) > 0
