from modules.settings import LOG_LEVEL, LOG_PATH, LOG_NAME
import logging


LOGGER_LEVEL = {
    'debug': logging.DEBUG,
    'info': logging.INFO
}.get(LOG_LEVEL)


def initialize_logger(logger_name: str = None):
    logging.basicConfig(
        format='%(asctime)s %(name)s %(levelname)s: %(message)s',
        datefmt='%H:%M:%S',
        filename=LOG_PATH, 
        filemode='a',
        level=LOGGER_LEVEL
    )
    return logging.getLogger(name=f'{LOG_NAME}:{logger_name}' if logger_name else LOG_NAME)

def start_run(logger):
    logger.info('---RUN STARTED---')

def close_logger(logger):
    logger.info('---RUN FINISHED---')

