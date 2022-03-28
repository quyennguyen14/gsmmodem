import logging
from logging.handlers import TimedRotatingFileHandler
import os
from pathlib import Path


def nlogger(string, filename, log_type='info'):
    log_arr = ['info', 'warning', 'error', 'critical', 'debug']

    cur_path = os.path.dirname(__file__)
    new_path = os.path.join(cur_path, '..', 'logs')

    log_file = new_path + '/' + filename + ".log"

    logHandler = TimedRotatingFileHandler(Path(log_file), when="D", interval=1, encoding="utf-8")
    logFormatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    logHandler.setFormatter(logFormatter)
    logger = logging.getLogger('MyLogger')

    if (logger.hasHandlers()):
        logger.handlers.clear()
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)

    try:
        if log_type.lower() not in log_arr:
            return Exception

        if log_type.lower() == 'info':
            logger.info(string)
        elif log_type.lower() == 'warning':
            logger.warning(string)
        elif log_type.lower() == 'error':
            logger.error(string)
        elif log_type.lower() == 'critical':
            logger.critical(string)
        else:
            logger.debug(string)

    except Exception:
        return -1

