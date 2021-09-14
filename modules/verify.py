import json
from modules.settings import PATHS
from hashlib import md5
from modules.ftp import connect
from modules.data import PRX_DATA_LIST
from colorama import Fore, Style
from mutagen.wave import WAVE


class Hash_Verifier:
    LOCAL_PATH = PATHS.LOCAL_PATH
    CACHED_HASHES_FILE = 'cached_hashes.json'

    def __init__(self, ftp_server, remote_dir, match_list=None) -> None:
        self.ftp_server = ftp_server
        self.remote_dir = remote_dir
        self.show_match_list = match_list  # uses .match_show method
        self.cached_hashes = self._read_cached_hashes() or {}
    
    # Main
    def check_hashes(self):
        hash_doesnt_match_list = []
        for each_file in self.LOCAL_PATH.iterdir():
            file_name = each_file.name
            if self.match_show(file_name):

                remote_hash = self.hash_remote(file_name)
                local_hash = self.hash_local(file_name) or remote_hash

                if remote_hash != local_hash:
                    hash_doesnt_match_list.append(file_name)
        
        self._write_cached_hashes()
        return hash_doesnt_match_list

    def match_show(self, file_name):
        # duplicated in Process class.
        return any(
            bool(show_match_str in file_name)
            for show_match_str in self.show_match_list
        )

    def hash_remote(self, file_name: str) -> str:
        if self.in_cache(file_name):
            return self.cached_hashes.get(file_name)

        md5_hash = md5()
        self.ftp_server.retrbinary(
            f'RETR /{self.remote_dir}/{file_name}', md5_hash.update
            )
        file_hash = md5_hash.hexdigest()
        self.cached_hashes.update({file_name: file_hash})
        return file_hash
    
    def hash_local(self, file_name: str) -> str:
        local_file_path = self.LOCAL_PATH.joinpath(file_name)
        if not local_file_path.exists():
            return None
        with open(local_file_path, 'rb') as local_file:
            file_contents = local_file.read()
            return md5(file_contents).hexdigest()

    def in_cache(self, file_name):
        return file_name in self.cached_hashes.keys()

    def _read_cached_hashes(self):
        if not self.LOCAL_PATH.joinpath(self.CACHED_HASHES_FILE).exists():
            return None
        with open(self.LOCAL_PATH.joinpath(self.CACHED_HASHES_FILE), 'r') as infile:
            try:
                return json.load(infile)
            except json.JSONDecodeError:
                return None

    def _write_cached_hashes(self):
        with open(self.LOCAL_PATH.joinpath(self.CACHED_HASHES_FILE), 'w+') as outfile:
            json.dump(self.cached_hashes, outfile)

class Segment_Verifier:
    PROCESSED_DIR = PATHS.FOR_DROPBOX
    LOWER_TOLERANCE = 3
    UPPER_TOLERANCE = 1

    def __init__(self, show_data) -> None:
        self.show_data = show_data
    
    def verify_show(self) -> list:
        mistimed_files = []
        add_segments_list = []
        single_segments_list = []
        # if not in add, check time
        # if in add, add and compare files in add_list
        #   if added files in list are not correct time, add to mistimed files
        # add all mistimed files to mistimed_files

        for wav_file in self.PROCESSED_DIR.iterdir():
            cut_number = self._get_cut_number(wav_file)
            if cut_number in self.show_data.timings.keys():
                single_segments_list.append(wav_file)
            if cut_number in self.show_data.add:
                add_segments_list.append(wav_file)
        
        for single_file in single_segments_list:
            if not self.is_correct_timing(single_file):
                mistimed_files.append(single_file)

        if not self._is_added_segments_timing_correct(add_segments_list):
            for added_file in add_segments_list:
                mistimed_files.append(added_file)

        return mistimed_files

    def _is_added_segments_timing_correct(self, add_list:list) -> bool:
        if len(add_list) != len(self.show_data.add):
            # if we don't have all the files, we can't add them all for time
            return True
        sum_in_seconds = sum([self._get_length(wav_file) for wav_file in add_list])
        return self.compare_time(self.show_data.add_time_target, sum_in_seconds)

    def is_correct_timing(self, wav_file):
        cut_number = self._get_cut_number(wav_file)
        target = self.show_data.timings.get(cut_number)
        actual = self._get_length(wav_file)
        return self.compare_time(target, actual)

    def compare_time(self, target_time: int, actual_time: int) -> bool:
        upper_limit = target_time + self.UPPER_TOLERANCE
        lower_limit = target_time - self.LOWER_TOLERANCE
        return lower_limit <= actual_time <= upper_limit

    def _get_cut_number(self, wav_file) -> str:
        return wav_file.stem.split('_')[0]

    def _get_length(self, wav_file) -> int:
        return int(WAVE(wav_file).info.length)


def check_hashes():
    ftp_server = connect()
    for show_data in PRX_DATA_LIST:
        verifier = Hash_Verifier(
            ftp_server, remote_dir=show_data.remote_dir, match_list=show_data.show_match
            )
        bad_hashes = verifier.check_hashes()

        if not bad_hashes:
            print(Fore.GREEN, 'Downloaded files have been verified ✓', Style.RESET_ALL)
            return

        for segment in bad_hashes:
            print('\nCORRUPTED FILE: ', end='', flush=True)
            print(Fore.RED, Style.BRIGHT, segment, Style.RESET_ALL, end='', flush=True)
            print(' has been corrupted.')


def _find_mistimed_files():
    mistimed_files = []
    for show_data in PRX_DATA_LIST:
        one_mistimed_file_list = Segment_Verifier(show_data).verify_show()
        if one_mistimed_file_list:
            for each_mistimed_file in one_mistimed_file_list:
                mistimed_files.append(each_mistimed_file)
    return mistimed_files


def _print_mistimed_files(mistimed_list):
    for segment in mistimed_list:
        print('MIS-TIMED FILE: ', end='', flush=True)
        print(Fore.RED, Style.BRIGHT, segment.name, Style.RESET_ALL, end='', flush=True)
        print('is not timed correctly')


def check_segments():
    mistimed_files = _find_mistimed_files()
    if not mistimed_files:
        print(Fore.GREEN, 'Processed file times have been verified ✓', Style.RESET_ALL)
        return

    _print_mistimed_files(mistimed_files)
    return mistimed_files