import os
import shutil
import subprocess
from modules.settings import LOCAL_PATH, FOR_DROPBOX, FOR_FFA


class Reveal:
    NUMBER_OF_SHOW_FILES = 9
    SHOW_MATCH = ['RevealWk_']
    SEGMENT_MATCHES = {
        'PROM01': 'promo',
        'SGMT01': 'billboard',
        'SGMT03': 'segment_a',
        'SGMT05': 'segment_b',
        'SGMT07': 'segment_c',
        'SGMT02': 'music_bed_a',
        'SGMT04': 'music_bed_b',
        'SGMT06': 'music_bed_c'
    }
    CUT_NUMBERS = {
        'promo': '17984',
        'billboard': '17978',
        'segment_a': '17979',
        'segment_b': '17981',
        'segment_c': '17983',
        'music_bed_a': '17980',
        'music_bed_b': '17982'
        # 'music_bed_c': ''
    }
    LOCAL_PATH = LOCAL_PATH
    FOR_DROPBOX = FOR_DROPBOX
    FOR_FFA = FOR_FFA
    
    def __init__(self):
        self.show_string = str(self.__class__.__name__).replace('_', ' ')
        self.file_list = self.get_file_list()
        self.source_paths = self.get_source_paths()
        self.destination_paths = self.get_destination_paths()
    
    def process(self):
        self.process_for_dropbox()
        self.process_for_ffa()
    
    def process_for_dropbox(self):
        # add date info to title.
        for segment_name in self.CUT_NUMBERS.keys():
            source_file = self.source_paths.get(segment_name)
            destination_file = self.destination_paths.get(segment_name)
            if source_file and source_file.exists():
                print(f'Writing {source_file.name} to {destination_file.parent.stem}')
                shutil.copy(
                    str(source_file),
                    str(self.destination_paths.get(segment_name))
                )
    
    def process_for_ffa(self):
        # use lame?
        # add date informtion to file name
        source_file = self.source_paths.get('promo')
        if source_file and source_file.exists():
            if os.name == 'nt':
                ffa_path = self.FOR_FFA.joinpath(
                    f'{self.show_string} PROMO{source_file.suffix}'
                    )
                print(f'Writing {ffa_path.name} to {ffa_path.parent.stem}')
                shutil.copy(
                    str(source_file),
                    str(ffa_path)
                )
            else:
                ffa_path = self.FOR_FFA.joinpath(f'{self.show_string} PROMO.mp3')
                print(f'Writing {ffa_path.name} to {ffa_path.parent.stem}')
                subprocess.run([
                    'ffmpeg', 
                    '-i', str(source_file), 
                    '-vn', 
                    '-ar', '44100', 
                    '-ac', '2', 
                    '-b:a', '192k',
                    '-y',
                    str(ffa_path)
                    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                # ffmpeg -i input-file.wav -vn -ar 44100 -ac 2 -b:a 192k output-file.mp3

    def get_destination_paths(self):
        return {
            segment: self.get_dropbox_file_name(segment, extension=file_path.suffix)
            for segment, file_path in self.source_paths.items()
        }

    def get_dropbox_file_name(self, segment_name, extension = '.wav'):
        segment_string = segment_name.replace('_', ' ').upper()

        return self.FOR_DROPBOX.joinpath(
            f'{self.CUT_NUMBERS.get(segment_name)}_{self.show_string} {segment_string}{extension}'
            )
    
    def get_file_list(self):
        file_list = [
            file_path for file_path in self.LOCAL_PATH.iterdir()
            if self.match_show(file_path.name)
            ]
        assert len(file_list) <= self.NUMBER_OF_SHOW_FILES, (
            f'Too many files for show, {self.show_string}'
            )
        return file_list

    def match_show(self, file_name):
        return any((show_match_str in file_name) for show_match_str in self.SHOW_MATCH)
    
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
        return f'-----{self.show_string}-----\n' + str(self.source_paths)


class Latino_USA(Reveal):
    SHOW_MATCH = [str(num) for num in range(35232, 35249)]
    NUMBER_OF_SHOW_FILES = 9
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


class Says_You(Reveal):
    SHOW_MATCH = ['SaysYou1_']
    NUMBER_OF_SHOW_FILES = 6
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


class The_Moth(Reveal):
    SHOW_MATCH = ['THEMOTH_']
    NUMBER_OF_SHOW_FILES = 7
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


class Snap_Judgment(Reveal):
    SHOW_MATCH =[str(num) for num in range(14155, 14162)]
    NUMBER_OF_SHOW_FILES = 7
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


PROGRAM_LIST = [
    Reveal,
    Latino_USA,
    Says_You,
    The_Moth,
    Snap_Judgment
]