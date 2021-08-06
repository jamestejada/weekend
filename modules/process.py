from colorama import Fore, Style
from modules.data import DATA_LIST, Show
from modules.settings import PATHS
from datetime import datetime, timedelta

class Audio:
    def __init__(
        self, sample_rate:int=44100, 
        target_level:float=-24.0, true_peak:float=-3.0, bitrate:str='256k'
        ) -> None:
        pass


class Process(Audio):
    LOCAL_PATH = PATHS.LOCAL_PATH
    FOR_DROPBOX = PATHS.FOR_DROPBOX
    FOR_FFA = PATHS.FOR_FFA

    def __init__(
        self, show_data:Show, process_list:list=None, threading:bool=False, _local_path=None,
        _destination_path=None
        ) -> None:
        
        self.local_path = _local_path or self.LOCAL_PATH
        self.destination_path  = _destination_path or self.FOR_DROPBOX

        self.process_list = process_list
        self.show_string = show_data.show_name
        self.show_match_strings = show_data.show_match
        self.max_number_of_files = show_data.number_of_files
        self.segment_match = show_data.segment_match
        self.cut_numbers = show_data.cut_numbers

        self.air_days_string = self.get_days_string(show_data.air_days)

        self.file_list = self.get_file_list(process_list=self.process_list)
        self.source_paths = self.get_source_paths()
        self.destination_paths = self.get_destination_paths()



    def get_file_list(self, process_list=None):
        """Returns the list to be processed. Either:
            1. the matching show files in LOCAL_PATH or
            2. the process_list passed in of files that have just been downloaded.
        """
        local_dir_list = self._local_dir_files()
        downloaded_list = self._get_downloaded_file_list(process_list=process_list)
        return downloaded_list or local_dir_list

    def _get_downloaded_file_list(self, process_list=None) -> list:
        if not process_list:
            return []
        return [
            self.local_path.joinpath(file_path.name)
            for file_path in process_list
            if self.match_show(file_path.name)
        ]

    def _local_dir_files(self) -> list:
        directory_list = [
            file_path for file_path in self.local_path.iterdir()
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
    
    def get_source_paths(self):
        """Returns a dictionary with segment name as key
        and the local file path as a value
        EXAMPLE:
        {
            'billboard': Path('./weekend/files/downloads/RevealWk_270_SGMT01.wav)',
            'segment_a': Path('./weekend/files/downloads/RevealWk_270_SGMT03.wav)',
            'segment_b': Path('./weekend/files/downloads/RevealWk_270_SGMT05.wav)',
            'segment_c': Path('./weekend/files/downloads/RevealWk_270_SGMT07.wav)'
        }
        """
        return {
            self.segment_match.get(match_string): file_path
            for file_path in self.file_list
            for match_string in self.segment_match.keys()
                if match_string in file_path.name
        }
    
    def get_destination_paths(self):
        """Returns dictionary of destination paths 
        {
            'billboard': Path('./weekend/files/for_dropbox/RevealWk_270_SGMT01.wav'),
            'segment_a': Path('./weekend/files/for_dropbox/RevealWk_270_SGMT03.wav'),
            'segment_b': Path('./weekend/files/for_dropbox/RevealWk_270_SGMT05.wav'),
            'segment_c': Path('./weekend/files/for_dropbox/RevealWk_270_SGMT05.wav')
        }
        """
        return {
            segment_name: self._get_dropbox_path(
                segment_name=segment_name, extension=file_path.suffix
                )
            for segment_name, file_path in self.source_paths.items()
        }

    def _get_dropbox_path(self, segment_name, extension='.wav'):
        """ Returns the destination path for DROPBOX files.
        """
        segment_string = segment_name.replace('_', ' ').upper()
        return self.destination_path.joinpath(
            f'{self.cut_numbers.get(segment_name)}_{self.show_string} '
            + f'{segment_string} {self.air_days_string}{extension}'
            )
    

