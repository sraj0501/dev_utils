import logging
import os.path
from functools import wraps
import sys
import inspect
from datetime import datetime

curr_dt = str(datetime.now().date())

def log_module(log_folder:str = None) -> logging:
    logger = logging.getLogger(__name__)
    if logger.handlers:
        return logger

    if os.path.exists(log_folder):
        f_name=os.path.join(log_folder, curr_dt)
    else:
        f_name = os.path.join("/tmp/", curr_dt)
    formatter = logging.Formatter('%(levelname)s: [%(asctime)s]::%(message)s')

    f_handler = logging.FileHandler(f_name)
    str_handler = logging.StreamHandler(sys.stdout)

    str_handler.setFormatter(formatter)
    f_handler.setFormatter(formatter)

    logger.addHandler(f_handler)
    logger.addHandler(str_handler)

    logger.setLevel(logging.DEBUG)

    # Return the parent frame, calling the logging module
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    module_name = module.__name__ if module else 'Unknown'
    logger.info(f"Started for module {module_name}")

    return logger


def timerfunc(func):
    start_time = datetime.now()
    logger = log_module()
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        logger.debug(f"Function took {datetime.now() - start_time} seconds.")
        return result
    return wrapper