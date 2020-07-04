import logging
from datetime import datetime


def set_custom_log_info(filename):
    logging.basicConfig(filename=filename, level=logging.INFO)


def info(e):
    logging.info(str(datetime.now()) + ": " + str(e))


def report(e: Exception):
    logging.exception(str(datetime.now()) + ": " + str(e))
