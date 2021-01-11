from settings import USERNAME, PASSWORD, IP
from ftplib import FTP

TIME_OUT = 3

# I probably don't need a class.
# class Server:
#     USERNAME = USERNAME
#     PASSWORD = PASSWORD
#     IP = IP
#     TIME_OUT = 3

#     def connect(self):
#         if n > self.TIME_OUT:
#             return
        
#         server = FTP(self.IP)
#         result = server.login(self.USERNAME, self.PASSWORD)

#         if '230' in result:
#             print(f'--------FTP CONNECTED--------')
#             return server
#         else:
#             self.FTP_connect(host, username, password, n+1)

def connect(n=1):
    if n > TIME_OUT:
        return

    server = FTP(IP)
    result = server.login(USERNAME, PASSWORD)
    if '230' in result:
        print('--------FTP CONNECTED--------')
        return server
    else:
        # does this interfere with lindear backoff....
        connect(n=n+1)