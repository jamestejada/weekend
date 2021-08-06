from modules.logger import initialize_logger
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from ffmpeg_normalize import FFmpegNormalize
from modules.settings import LOCAL_PATH, FOR_DROPBOX, FOR_FFA, Execution_Flags
import os
import subprocess


class Process_BASE:
    """ This class finds downloaded files for a specific program, 
    processes them (normalize to -24 LUFs and/or convert to mp3),
    and renames for ENCO Dropbox or FFA network drive (for remote hosts).
    """
    NUMBER_OF_SHOW_FILES = None
    SHOW_MATCH = None
    AIR_DAYS = None
    SEGMENT_MATCHES = None
    CUT_NUMBERS = None

    LOCAL_PATH = LOCAL_PATH
    FOR_DROPBOX = FOR_DROPBOX
    FOR_FFA = FOR_FFA

    def __init__(
        self, process_list=None, sample_rate=44100, target_level=-24.0,
        true_peak=-3.0, bitrate='256k', threading=False
        ):
        self.logger = initialize_logger(self.__class__.__name__)

        self.show_string = str(self.__class__.__name__).replace('_', ' ')
        self.air_days_string = self.get_days_string()

        self.process_list = process_list

        self.file_list = self.get_file_list(process_list=self.process_list)
        self.source_paths = self.get_source_paths()
        self.destination_paths = self.get_destination_paths()

        self.threading = threading
        self.dry_run = Execution_Flags.DRY_RUN
        self.force = Execution_Flags.FORCE_PROCESS

        self.target_level = target_level
        self.sample_rate = sample_rate
        self.true_peak = true_peak
        self.bitrate = bitrate

        for var, value in self.__dict__.items():
            self.logger.debug(f'{var}: {value}')

    # main
    def process(self):
        self.process_for_dropbox()
        self.process_for_ffa()
    
    def get_days_string(self):
        """returns a string containing formatted air dates
        of form: 'Jan 24'. This also accounts for two or more
        air days set in the self.AIR_DAYS(list) class variable.
        If two or more air dates are given, this method joins
        them with an 'and.' 

        eg. "Jan 23 and Jan 24"
        """
        today = datetime.today()
        monday = today - timedelta(days=today.weekday())
        air_date_list = [
            (monday + timedelta(days=day)).strftime('%b %-d')
            for day in self.AIR_DAYS
            ]
        return ' and '.join(air_date_list)
    
    def process_for_dropbox(self):
        """ Prepares files for ENCO Dropbox. This method
        normalizes and renames files to be ingested into
        DAD system with specific metadata.

        If a file to be written already exists, it will
        skip that file. 
        """
        if self.threading:
            with ThreadPoolExecutor() as executor:
                executor.map(
                    self.normalize,
                    [self.source_paths.get(segment) for segment in self.CUT_NUMBERS.keys()],
                    [self.destination_paths.get(segment) for segment in self.CUT_NUMBERS.keys()]
                    )
            return

        for segment_name in self.CUT_NUMBERS.keys():
            source = self.source_paths.get(segment_name)
            destination = self.destination_paths.get(segment_name)

            if self.dry_run and destination:
                self._message(destination)
                print()
            elif source and source.exists():
                self.normalize(source, destination)

    def _should_skip(self, destination):
        return all([
            destination, 
            destination.exists(),
            not self.force,
            not self.process_list
        ])

    def normalize(self, source, destination):
        if self._should_skip(destination):
            return

        if not self.threading:
            self._message(destination)

        norm = FFmpegNormalize(
            target_level=self.target_level,
            sample_rate=self.sample_rate,
            true_peak=self.true_peak,
            video_disable=True
        )
        norm.add_media_file(source, destination)
        norm.run_normalization()

        if self.threading:
            self._message(destination)
        self._done_message()

    def process_for_ffa(self, key='promo'):
        # source is a for_dropbox path to use already normalized files
        source = self.destination_paths.get(key)
        key_string = str(key).replace('_', ' ').upper()
        extension = '.wav' if os.name == 'nt' else '.mp3'
        file_name = f'{self.show_string} {key_string} {self.air_days_string}{extension}'
        destination = self.FOR_FFA.joinpath(file_name)

        if self.dry_run and destination and key in self.source_paths.keys():
            self._message(destination)
            print()
        elif source and source.exists():
            conversion_func = self.normalize if os.name == 'nt' else self.convert_to_mp3
            conversion_func(source, destination)

    def _message(self, destination_path):
        print(
            f'Writing "{destination_path.name}" to "{destination_path.parent.stem}"...',
            end='', flush=True
            )

    def _done_message(self):
        print(Fore.GREEN, 'DONE', Style.RESET_ALL)

    def convert_to_mp3(self, source, destination):
        if self._should_skip(destination):
            return

        self._message(destination)
        subprocess.run(
            [
                'ffmpeg', '-i', str(source), '-vn', '-ar', str(self.sample_rate),
                '-ac', '2', '-b:a', self.bitrate, '-y',
                str(destination)
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        self._done_message()

    def get_destination_paths(self):
        return {
            segment: self.get_dropbox_path(segment, extension=file_path.suffix)
            for segment, file_path in self.source_paths.items()
        }

    def get_dropbox_path(self, segment_name, extension='.wav'):
        """ Returns the destination path for DROPBOX files.
        """
        segment_string = segment_name.replace('_', ' ').upper()

        return self.FOR_DROPBOX.joinpath(
            f'{self.CUT_NUMBERS.get(segment_name)}_{self.show_string} '
            + f'{segment_string} {self.air_days_string}{extension}'
            )
    
    def get_file_list(self, process_list=None):

        downloaded_list = [
                self.LOCAL_PATH.joinpath(file_name)
                for file_name in process_list or []
                if self.match_show(file_name)
            ]
        directory_list = [
                file_path for file_path in self.LOCAL_PATH.iterdir()
                if self.match_show(file_path.name)
            ]
        try:
            assert len(directory_list) <= self.NUMBER_OF_SHOW_FILES, (
                f'Too many files for show, {self.show_string}'
                )
        except AssertionError as e:
            print(Fore.RED, Style.BRIGHT, 'ERROR: ', e, Style.RESET_ALL)
            print('\n'.join(file_name.name for file_name in directory_list))
            self.logger.warn(f'ERROR: {e}')
            return []
        return downloaded_list if process_list else directory_list

    def match_show(self, file_name):
        return any(
            (show_match_str in file_name)
            for show_match_str in self.SHOW_MATCH
            )
    
    def get_source_paths(self):
        """Returns a dictionary with segment name as key
        and the file path as a value

        EXAMPLE:
        {
            'billboard': './downloads/RevealWk_270_SGMT01.wav',
            'segment_a': './downloads/RevealWk_270_SGMT03.wav',
            'segment_b': './downloads/RevealWk_270_SGMT05.wav',
            'segment_c': './downloads/RevealWk_270_SGMT07.wav'
        }
        """
        return {
            self.SEGMENT_MATCHES.get(match_string): file_path
            for file_path in self.file_list
            for match_string in self.SEGMENT_MATCHES.keys() if match_string in file_path.name
        }
    
    def __str__(self):
        return f'-{self.show_string}-\n' + str(self.source_paths)


class Reveal(Process_BASE):
    NUMBER_OF_SHOW_FILES = 9
    SHOW_MATCH = ['RevealWk_']
    AIR_DAYS = [4]
    SEGMENT_MATCHES = {
        'PROM01': 'promo',
        'SGMT01': 'billboard',
        'SGMT03': 'segment_a',
        'SGMT05': 'segment_b',
        'SGMT07': 'segment_c',
        'SGMT04': 'music_bed_a',
        'SGMT06': 'music_bed_b',
        'SGMT02': 'music_bed_C'
    }
    CUT_NUMBERS = {
        'promo': '17984',
        'billboard': '17978',
        'segment_a': '17979',
        'segment_b': '17981',
        'segment_c': '17983',
        'music_bed_a': '17980',
        'music_bed_b': '17982'
        # 'music_bed_c': 'NOT USED'
    }


class Latino_USA(Process_BASE):
    SHOW_MATCH = [str(num) for num in range(35232, 35249)]
    NUMBER_OF_SHOW_FILES = 9
    AIR_DAYS = [6]
    SEGMENT_MATCHES = {
        '35232': 'promo',
        '35242': 'billboard',
        '35244': 'segment_a',
        '35246': 'segment_b',
        '35248': 'segment_c',
        '35243': 'music_bed_a',
        '35245': 'music_bed_b',
        '35247': 'music_bed_c'
    }
    CUT_NUMBERS = {
        'promo': '75292',
        'billboard': '17030',
        'segment_a': '17032',
        'segment_b': '17034',
        'segment_c': '17036',
        'music_bed_a': '17031',
        'music_bed_b': '17033',
        'music_bed_c': '17035'
    }


class Says_You(Process_BASE):
    SHOW_MATCH = ['SaysYou1_']
    NUMBER_OF_SHOW_FILES = 6
    AIR_DAYS = [6]
    SEGMENT_MATCHES = {
        'PROM01': 'promo',
        'SGMT01': 'billboard',
        'SGMT02': 'segment_a',
        'SGMT03': 'segment_b',
        'SGMT04': 'segment_c',
    }
    CUT_NUMBERS = {
        'promo': '27305',
        'billboard': '27300',
        'segment_a': '27301',
        'segment_b': '27302',
        'segment_c': '27303'        
    }


class The_Moth(Process_BASE):
    SHOW_MATCH = ['THEMOTH_']
    NUMBER_OF_SHOW_FILES = 7
    AIR_DAYS = [6]
    SEGMENT_MATCHES = {
        'PROM01': 'promo',
        'SGMT01': 'billboard',
        'SGMT02': 'segment_a',
        'SGMT04': 'segment_b',
        'SGMT06': 'segment_c',
        'SGMT03': 'music_bed_a',
        'SGMT05': 'music_bed_b'

    } 
    CUT_NUMBERS = {
        'promo': '14172',
        'billboard': '14166',
        'segment_a': '14167',
        'segment_b': '14169',
        'segment_c': '14171',
        'music_bed_a': '14168',
        'music_bed_b': '14170'
    }


class Snap_Judgment(Process_BASE):
    SHOW_MATCH =[str(num) for num in range(14155, 14162)]
    NUMBER_OF_SHOW_FILES = 7
    AIR_DAYS = [6]
    SEGMENT_MATCHES = {
        '14161': 'promo',
        '14155': 'billboard',
        '14156': 'segment_a',
        '14158': 'segment_b',
        '14160': 'segment_c',
        '14157': 'music_bed_a',
        '14159': 'music_bed_b'
    }
    CUT_NUMBERS = {
        'promo': '14161',
        'billboard': '14155',
        'segment_a': '14156',
        'segment_b': '14158',
        'segment_c': '14160',
        'music_bed_a': '14157',
        'music_bed_b': '14159'
    }


class This_American_Life(Process_BASE):
    SHOW_MATCH = ['ThisAmer_']
    NUMBER_OF_SHOW_FILES = 5
    AIR_DAYS = [5, 6]
    SEGMENT_MATCHES = {
        'PROM01': 'promo',
        'PROM02': 'promo_today',
        'SGMT01': 'segment_a',
        'SGMT03': 'segment_b',
        'SGMT02': 'music_bed_a'
    }
    CUT_NUMBERS = {
        'promo': '25321',
        'segment_a': '17040',
        'segment_b': '17042',
        'music_bed_a': '17041'
    }
