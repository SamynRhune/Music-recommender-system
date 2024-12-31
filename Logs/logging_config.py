import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name, log_file):
    handler = RotatingFileHandler(f'logs/{name}.log', maxBytes=5*1024*1024, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger