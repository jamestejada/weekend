from modules.logger import initialize_logger
from colorama import Fore, Style
from modules.settings import PRX
from ftplib import FTP


TIME_OUT = 3


def connect(n=1):
    logger = initialize_logger('FTP')
    logger.debug(f'TIME_OUT = {TIME_OUT}')
    logger.debug(f'n = {n}')

    if n > TIME_OUT:
        return

    print(Fore.YELLOW, 'FTP CONNECTING...', end='', flush=True)

    server = FTP(PRX.IP)
    result = server.login(PRX.USERNAME, PRX.PASSWORD)
    if '230' in result:
        print(Fore.GREEN, Style.BRIGHT, result, Style.RESET_ALL)
        return server
    else:
        # does this interfere with linear backoff....?
        connect(n=n+1)
