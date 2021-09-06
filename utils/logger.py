import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s -  %(message)s')


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    return logger
