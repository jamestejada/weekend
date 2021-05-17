import json
from hashlib import md5
from mutagen.wave import WAVE
from modules.settings import LOCAL_PATH, FOR_DROPBOX
from modules import process
from modules.ftp import connect
from colorama import Style, Fore


class Hash_Verifier:
    LOCAL_PATH = LOCAL_PATH
    CACHED_HASHES_FILE = 'cached_hashes.json'

    def __init__(self, ftp_server, remote_dir, processor_class=None) -> None:
        self.ftp_server = ftp_server
        self.remote_dir = remote_dir
        self.processor = processor_class  # uses .match_show method
        self.cached_hashes = self._read_cached_hashes() or {}
    
    # Main
    def check_hashes(self):
        hash_doesnt_match_list = []
        for each_file in self.LOCAL_PATH.iterdir():
            file_name = each_file.name
            if self.processor().match_show(file_name):

                remote_hash = self.hash_remote(file_name)
                local_hash = self.hash_local(file_name) or remote_hash

                if remote_hash != local_hash:
                    hash_doesnt_match_list.append(file_name)
        
        self._write_cached_hashes()
        return hash_doesnt_match_list
    
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
    TIMINGS = None
    ADD = None
    ADD_TIME_TARGET = None

    PROCESSED_DIR = FOR_DROPBOX
    LOWER_TOLERANCE = 3
    UPPER_TOLERANCE = 1

    def __init__(self) -> None:
        self.add_list = []
    # pass time verification if not all segments are there.
    # use check class?

    # Main
    def verify_show(self) -> list:
        mistimed_files = []
        for wav_file in self.PROCESSED_DIR.iterdir():
            cut_number = self._get_cut_number(wav_file)
            if cut_number in self.TIMINGS.keys():
                if not self.is_correct_timing(wav_file):
                    mistimed_files.append(wav_file)                    
            if cut_number in self.ADD:
                self.add_list.append(wav_file)
        if not self.is_added_segments_timing_correct(self.add_list):
            for segment in self.add_list:
                mistimed_files.append(segment)
        return mistimed_files
    
    def is_added_segments_timing_correct(self, add_list: list) -> bool:
        if len(add_list) != len(self.ADD):
            # If not all added segment files are delivered, 
            # we can't compare times.
            return True
        sum_in_secs = sum([self._get_length(wav_file) for wav_file in add_list])
        return self.compare_time(self.ADD_TIME_TARGET, sum_in_secs)
    
    def compare_time(self, target_time: int, actual_time: int):
        """Checks if actual time is within tolerances of target time"""
        upper_limit = target_time + self.UPPER_TOLERANCE
        lower_limit = target_time - self.LOWER_TOLERANCE
        return lower_limit <= actual_time <= upper_limit
    
    def _get_cut_number(self, wav_file):
        return wav_file.stem.split('_')[0]
    
    def is_correct_timing(self, wav_file):
        cut_number = self._get_cut_number(wav_file)
        target = self.TIMINGS.get(cut_number)
        actual = self._get_length(wav_file)
        return self.compare_time(target, actual)

    def _get_length(self, wav_file):
        return int(WAVE(wav_file).info.length)

class Reveal(Segment_Verifier):
    TIMINGS = {
        '17984': 30,
        '17978': 60,
        '17980': 60,
        '17982': 60
    }
    ADD_TIME_TARGET = 3060
    ADD = [
        '17979',
        '17981',
        '17983'
    ]


class Latino_USA(Segment_Verifier):
    TIMINGS = {
        '75292': 30,
        '17030': 60,
        '17031': 30,
        '17033': 60,
        '17035': 60
    }
    ADD_TIME_TARGET = 3030
    ADD = [
        '17032',
        '17034',
        '17036'
    ]


class Says_You(Segment_Verifier):
    TIMINGS = {
        '27305': 30,
        '27300': 60
    }
    ADD_TIME_TARGET = 3000
    ADD = [
        '27301',
        '27302',
        '27303'
    ]


class The_Moth(Segment_Verifier):
    TIMINGS = {
        '14172': 30,
        '14166': 60,
        '14168': 60,
        '14170': 60
    }
    ADD_TIME_TARGET = 3060
    ADD = [
        '14167',
        '14169',
        '14171'
    ]


class Snap_Judgment(Segment_Verifier):
    TIMINGS = {
        '14161': 30,
        '14155': 60,
        '14157': 90,
        '14159': 90
    }
    ADD_TIME_TARGET = 3000
    ADD = [
        '14156',
        '14158',
        '14160'
    ]


class This_American_Life(Segment_Verifier):
    TIMINGS = {
        '25321': 30,
        '17041': 60
    }
    ADD_TIME_TARGET = 3480
    ADD = [
        '17040',
        '17042'
    ]


segment_verifier_classes = [
    Reveal,
    Latino_USA,
    Says_You,
    The_Moth,
    Snap_Judgment,
    This_American_Life
]

hash_check_tuples = (
    #  remote_dir, processor
    ('LatinoUS', process.Latino_USA),
    ('RevealWk', process.Reveal),
    ('SaysYou1', process.Says_You),
    ('SnapJudg', process.Snap_Judgment),
    ('THEMOTH', process.The_Moth),
    ('ThisAmer', process.This_American_Life)
)

def check_hashes():
    ftp_server = connect()
    print()
    for remote_dir, processor in hash_check_tuples:
        verifier = Hash_Verifier(ftp_server, remote_dir, processor)
        bad_hashes = verifier.check_hashes()

        if not bad_hashes:
            print(Fore.GREEN, 'Downloaded files have been verified', Style.RESET_ALL)
            return

        for segment in bad_hashes:
            print('CORRUPTED FILE: ', end='', flush=True)
            print(Fore.RED, Style.BRIGHT, segment, Style.RESET_ALL, end='', flush=True)
            print(' has been corrupted.')

def check_segments():
    print()
    list_of_mistimed_file_lists = [
        print_mistimed_files_for_one_show(verifier) 
        for verifier in segment_verifier_classes
    ]
    if not any(list_of_mistimed_file_lists):
        print(Fore.GREEN, 'All file times have been verified', Style.RESET_ALL)
    print()

def print_mistimed_files_for_one_show(show_verifier):
    mistimed_list = show_verifier().verify_show()
    for segment in mistimed_list:
        print('MIS-TIMED FILE: ', end='', flush=True)
        print(Fore.RED, Style.BRIGHT, segment.name, Style.RESET_ALL, end='', flush=True)
        print('is not timed correctly')
    return mistimed_list or None
