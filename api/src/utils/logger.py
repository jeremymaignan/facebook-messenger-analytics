import logging
import os
from datetime import datetime

from utils.utils import get_conf

# Create a custom logger
log = logging.getLogger("api")

# Create handlers
filename = "{}/api_{}.log".format(get_conf("log_dir"), datetime.now().strftime('%Y_%m_%d_%H_%M'))
c_handler = logging.StreamHandler()
#f_handler = logging.FileHandler(filename)
c_handler.setLevel(getattr(logging, os.environ.get("LOG_LEVEL","INFO").upper()))
#f_handler.setLevel(getattr(logging, os.environ.get("LOG_LEVEL","INFO").upper()))

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
#f_format = logging.Formatter('%(asctime)s - %(name)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
#f_handler.setFormatter(f_format)

# Add handlers to the logger
#log.addHandler(c_handler)
#log.addHandler(f_handler)
