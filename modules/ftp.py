from modules.settings import PRX
from ftplib import FTP

TIME_OUT = 3


def connect(n=1):
    if n > TIME_OUT:
        return

    server = FTP(PRX.IP)
    result = server.login(PRX.USERNAME, PRX.PASSWORD)
    if '230' in result:
        print('--------FTP CONNECTED--------')
        print(result)
        return server
    else:
        # does this interfere with linear backoff....?
        connect(n=n+1)

