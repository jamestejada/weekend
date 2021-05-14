import json
from hashlib import md5
from mutagen.wave import WAVE
from modules.settings import LOCAL_PATH, FOR_DROPBOX

# next add a check in 'for_dropbox' folder for proper show lengths

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

    def verify_show(self):
        print(self.__class__.__name__)
        mistimed_files = []
        for wav_file in self.PROCESSED_DIR.iterdir():
            cut_number = self._get_cut_number(wav_file)
            if cut_number in self.TIMINGS.keys():
                if not self.is_correct_timing(wav_file):
                    mistimed_files.append(wav_file.name)
                    # append to file_name to output list
                    # to reprocess?
                    print(wav_file.name, 'is not good')
            if cut_number in self.ADD:
                self.add_list.append(wav_file)
        print(self.add_segments())
    
    def add_segments(self):
        if len(self.add_list) != len(self.ADD):
            # If not all added segment files are delivered, 
            # we can't compare times.
            return True
        sum_in_secs = sum([self._get_length(wav_file) for wav_file in self.add_list])
        return self.compare_time(self.ADD_TIME_TARGET, sum_in_secs)
    
    def compare_time(self, target_time: int, actual_time: int):
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


class Latino_USA:
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


class Says_You:
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

class The_Moth:
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


class Snap_Judgment:
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


class This_American_Life:
    TIMINGS = {
        '25321': 30,
        '17041': 60
    }
    ADD_TIME_TARGET = 3480
    ADD = [
        '17040',
        '17042'
    ]
