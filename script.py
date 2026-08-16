import logging
import logging.handlers
import time
import random

# Map of facility name to SysLogHandler facility constant
FACILITIES = {
    "local1": logging.handlers.SysLogHandler.LOG_LOCAL1,
    "local2": logging.handlers.SysLogHandler.LOG_LOCAL2,
    "local3": logging.handlers.SysLogHandler.LOG_LOCAL3,
}

SYSLOG_ADDRESS = "/dev/log"  # local syslog socket on Linux

def build_logger(name, facility):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.SysLogHandler(address=SYSLOG_ADDRESS, facility=facility)
    formatter = logging.Formatter(f"{name}: %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

loggers = {name: build_logger(name, fac) for name, fac in FACILITIES.items()}

sample_messages = [
    (logging.INFO, "service started successfully"),
    (logging.WARNING, "high memory usage detected"),
    (logging.ERROR, "failed to connect to backend"),
    (logging.DEBUG, "heartbeat check passed"),
    (logging.CRITICAL, "disk almost full"),
]

def send_test_events(count_per_facility=5, delay=1.0):
    for i in range(count_per_facility):
        for name, logger in loggers.items():
            level, msg = random.choice(sample_messages)
            logger.log(level, f"test event {i} - {msg}")
        time.sleep(delay)

if __name__ == "__main__":
    send_test_events()
