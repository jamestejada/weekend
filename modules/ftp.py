from colorama import Fore, Style
from modules.settings import PRX
from modules.choose import choose_files
from modules.download import Download_Files
from ftplib import FTP

TIME_OUT = 3


def connect(n=1):
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

FTP_DIR_LIST = [
    ('LatinoUS', 'Latino USA'),
    ('RevealWk', 'Reveal'),
    ('SaysYou1', 'Says You'),
    ('SnapJudg', 'Snap Judgment'),
    ('THEMOTH', 'The Moth'),
    ('ThisAmer', 'This American Life')
]


# main
def download_show_files():
    prx_server = connect()
    print()

    for ftp_dir, show_name in FTP_DIR_LIST:
        print()
        print(Fore.CYAN, f'-{show_name}-', Style.RESET_ALL)
        process_ftp_dir(prx_server, ftp_dir)
    
    prx_server.close()


def process_ftp_dir(prx_server, ftp_dir):
    file_info_generator = prx_server.mlsd(f'/{ftp_dir}')
    files_to_get = choose_files(ftp_dir, file_info_generator)

    download_files = Download_Files(prx_server, ftp_dir, files_to_get)
    download_files.download_all()
