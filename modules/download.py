from pathlib import Path
from modules.settings import LOCAL_PATH, DRY_RUN, SAT_PATH
from modules.logger import initialize_logger
from colorama import Style, Fore
import shutil


class Download_Files:

    LOCAL_PATH = LOCAL_PATH

    def __init__(self, server, remote_dir: str, download_list: list):
        self.logger = initialize_logger(self.__class__.__name__)
        
        self.download_list = download_list
        self.remote_dir = remote_dir
        self.server = server
        self.dry_run = DRY_RUN

        for var, value in self.__dict__.items():
            self.logger.debug(f'{var}: {value}')

    
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


class Sat_Download:

    LOCAL_PATH = LOCAL_PATH
    SAT_PATH = SAT_PATH

    def __init__(self, download_list: list):

        self.logger = initialize_logger(self.__class__.__name__)

        self.download_list = download_list
        self.dry_run = DRY_RUN

        for var, value in self.__dict__.items():
            self.logger.debug(f'{var}: {value}')

    def download_all(self):
        results = []
        for each_file in self.download_list:
            which_function = print if self.dry_run else self.download_one
            result = which_function(each_file)
            results.append(True if self.dry_run else result)
        self.logger.debug(f'download results: {results}')
        return results
    
    def download_one(self, one_file) -> bool:
        full_path = self.LOCAL_PATH.joinpath(one_file)
        full_sat_path = self.SAT_PATH.joinpath(one_file)
    
        print(f'Downloading {one_file}...', end='', flush=True)
        try:
            self.copy(full_sat_path, full_path)
            color = Fore.GREEN
            success = True
        except:
            color = Fore.RED
            success = False
        finally:
            print(color, 'SUCCESS' if success else 'FAILED', Style.RESET_ALL)
        return success

    def copy(self, remote_path: Path, local_path: Path):
        shutil.copy(str(remote_path), str(local_path))
