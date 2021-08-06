from colorama import Fore, Style
from modules.data import DATA_LIST, Show
from modules.settings import PATHS
from datetime import datetime, timedelta


class Process:
    LOCAL_PATH = PATHS.LOCAL_PATH
    FOR_DROPBOX = PATHS.FOR_DROPBOX
    FOR_FFA = PATHS.FOR_FFA

    def __init__(
        self, show_data:Show, process_list:list=None, sample_rate:int=44100,
        target_level:float=-24.0, true_peak:float=-3.0,
        bitrate:str='256k', threading:bool=False
        ) -> None:
        
        self.show_string = show_data.show_name
        self.show_match_strings = show_data.show_match
        self.max_number_of_files = show_data.number_of_files

        self.air_days_string = self.get_days_string(show_data.air_days)
        self.process_list = process_list

        self.file_list = self.get_file_list(process_list=self.process_list)


    def get_file_list(self, process_list=None, _local_path=None):
        """Returns the list to be processed. Either:
            1. the matching show files in LOCAL_PATH or
            2. the process_list passed in of files that have just been downloaded.
        """
        local_path = _local_path or self.LOCAL_PATH
        local_dir_list = self._local_dir_files(local_path)
        downloaded_list = self._get_downloaded_file_list(local_path, process_list=process_list)
        return downloaded_list or local_dir_list

    def _get_downloaded_file_list(self, local_path, process_list=None) -> list:
        if not process_list:
            return []
        return [
            local_path.joinpath(file_path.name)
            for file_path in process_list
            if self.match_show(file_path.name)
        ]

    def _local_dir_files(self, local_path) -> list:
        directory_list = [
            file_path for file_path in local_path.iterdir()
            if self.match_show(file_path.name)
        ]
        try:
            assert len(directory_list) <= self.max_number_of_files, (
                f'Too many files for show, {self.show_string}'
            )
        except AssertionError as e:
            print(Fore.RED, Style.BRIGHT, 'ERROR: ', e, Style.RESET_ALL)
            return []
        return directory_list

    def match_show(self, file_name) -> bool:
        """Returns whether or not a given file_name is a match for
        the current show being processed
        """
        return any(
            bool(show_match_str in file_name)
            for show_match_str in self.show_match_strings
            )
    
    def get_days_string(self, air_weekday_list:list):
        """Returns a string of the current air days with 3 char month and number day
        e.g. 'Jun 12', or 'Jun 12 and Jun 13'
        """
        today = datetime.today()
        monday = today - timedelta(days=today.weekday())
        air_date_list = [
            (monday + timedelta(days=day)).strftime('%b %-d')
            for day in air_weekday_list
        ]
        return ' and '.join(air_date_list)