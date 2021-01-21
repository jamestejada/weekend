from modules.settings import PRX
from modules.choose import choose_files
from modules.download import Download_Files
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


FTP_DIR_LIST = [
    'LatinoUS',
    'RevealWk',
    'SaysYou1',
    'SnapJudg',
    'THEMOTH',
    'ThisAmer'
]


# main
def download_show_files():
    prx_server = connect()

    for ftp_dir in FTP_DIR_LIST:
        process_ftp_dir(prx_server, ftp_dir)
    
    prx_server.close()


def process_ftp_dir(prx_server, ftp_dir):

    print(f'---{ftp_dir}---')

    file_info_generator = prx_server.mlsd(f'/{ftp_dir}')
    files_to_get = choose_files(ftp_dir, file_info_generator)

    download_files = Download_Files(prx_server, ftp_dir, files_to_get)
    download_files.download_all()
