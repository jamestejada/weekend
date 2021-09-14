from pathlib import Path
from modules.settings import PATHS, Execution_Flags
from modules.logger import initialize_logger
from modules.verify import Hash_Verifier
from colorama import Style, Fore
import shutil


class Download_Files(Hash_Verifier):

    LOCAL_PATH = PATHS.LOCAL_PATH

    def __init__(self, ftp_server, remote_dir: str, download_list: list):
        self.logger = initialize_logger(self.__class__.__name__)
        
        super().__init__(ftp_server, remote_dir)
        self.download_list = download_list
        # self.remote_dir = remote_dir
        # self.ftp_server = ftp_server
        self.dry_run = Execution_Flags.DRY_RUN

        for var, value in self.__dict__.items():
            self.logger.debug(f'{var.upper()}: {value}')

    
    def download_all(self):
        for each_file in self.download_list:
            which_function = print if self.dry_run else self.download_one
            which_function(each_file)
        self._write_cached_hashes()

    def download_one(self, one_file):
        full_path = self.LOCAL_PATH.joinpath(one_file)
        retr_string = f'RETR /{self.remote_dir}/{one_file}'

        with open(full_path, 'wb') as out_file:
            print(f'Downloading {one_file}...', end='', flush=True)
            result = self.ftp_server.retrbinary(retr_string, out_file.write)

        success = ('226' in result) and (
            self.hash_local(one_file) == self.hash_remote(one_file)
            )
        color, message = (
                Fore.GREEN, 'DOWNLOADED and VERIFIED'
            ) if success else (
                Fore.RED, f'NOT VERIFIED\n{self.hash_local(one_file)}\n{self.hash_remote(one_file)}'
                )

        print(color, message, Style.RESET_ALL)
        log_func = self.logger.debug if success else self.logger.warning
        log_func(f'{one_file}: {message}')

        return success

    # override
    def in_cache(self, file_name):
        # We want this function to alwyas return false within the 
        # Download_Files class because we want all newly downloaded files
        # To store a new hash in the hash cache when self.hash_remote is called.
        return False


class Sat_Download:

    LOCAL_PATH = PATHS.LOCAL_PATH
    SAT_PATH = PATHS.SAT_PATH

    def __init__(self, download_list: list):

        self.logger = initialize_logger(self.__class__.__name__)

        self.download_list = download_list
        self.dry_run = Execution_Flags.DRY_RUN

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
