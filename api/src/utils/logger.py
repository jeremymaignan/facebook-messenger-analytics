import logging
import os
from datetime import datetime

from utils.utils import get_conf


def add_file_handler():
    # Create a custom logger
    log = logging.getLogger("api")
    if os.environ.get("ENV", "LOCAL") == "PROD":
        # Create file handler
        filename = "{}/etl_{}.log".format(get_conf("log_dir"), datetime.now().strftime('%Y_%m_%d_%H_%M'))
        f_handler = logging.FileHandler(filename)
        f_handler.setLevel(getattr(logging, os.environ.get("LOG_LEVEL","INFO").upper()))
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s')
        f_handler.setFormatter(f_format)
        log.addHandler(f_handler)
    return log

log = add_file_handler()
