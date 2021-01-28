from modules.settings import LOCAL_PATH, DRY_RUN
from colorama import Style, Fore

class Download_Files:

    LOCAL_PATH = LOCAL_PATH

    def __init__(self, server, remote_dir: str, download_list: list):
        self.download_list = download_list
        self.remote_dir = remote_dir
        self.server = server
        self.dry_run = DRY_RUN
    
    def download_all(self):
        for each_file in self.download_list:
            which_function = print if self.dry_run else self.download_one
            which_function(each_file)

    def download_one(self, one_file):
        full_path = self.LOCAL_PATH.joinpath(one_file)

        with open(full_path, 'wb') as out_file:
            print(f'Downloading {one_file}...', end='', flush=True)
            result = self.server.retrbinary(
                f'RETR /{self.remote_dir}/{one_file}', out_file.write
                )
            success = '226' in result
            color = Fore.GREEN if success else Fore.RED
            print(color, 'SUCCESS' if success else 'FAILED', Style.RESET_ALL)
            return success


