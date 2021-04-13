from modules.settings import LOG_LEVEL, LOG_PATH
import logging

LOGGER_LEVEL = {
    'debug': logging.DEBUG,
    'info': logging.INFO
}.get(LOG_LEVEL)

def initialize_logger(logger_name: str):
    logging.basicConfig(
        filename=LOG_PATH, 
        filemode='a',
        format='%(asctime)s %(name)s %(level)s %(message)s',
        datefmt='%H:%M:%S',
        level=LOGGER_LEVEL
    )
    logger = logging.getLogger(logger_name)
    logger.info('---RUN STARTED---')
    return logger

def close_logger(logger):
    logger.info('---RUN FINISHED---')
    
