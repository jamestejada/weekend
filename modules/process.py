import shutil
from modules.settings import LOCAL_PATH, FOR_DROPBOX, FOR_FFA


class Reveal:
    SHOW_MATCH = ['RevealWk_']
    SEGEMENT_MATCHES = {
        'SGMT01': 'billboard',
        'SGMT03': 'segment_a',
        'SGMT05': 'segment_b',
        'SGMT07': 'segment_c',
        'PROM01': 'promo'
    }
    MUSIC_BEDS = {
        'SGMT02': 'music_a',
        'SGMT04': 'music_b',
        'SGMT06': 'music_c'
    }
    CUT_NUMBERS = {
        'billboard': '17978',
        'segment_a': '17979',
        'segment_b': '17981',
        'segment_c': '17983',
        'promo': '17984'
    }
    LOCAL_PATH = LOCAL_PATH
    FOR_DROPBOX = FOR_DROPBOX
    FOR_FFA = FOR_FFA
    
    def __init__(self):
        self.file_list = self.get_file_list()
        self.source_paths = self.get_source_paths()
        self.destination_paths = self.get_destination_paths()
    
    def process(self):
        self.process_for_dropbox()
        self.process_for_ffa()
    
    def process_for_dropbox(self):
        # add date info to title.
        for segment_name in self.CUT_NUMBERS.keys():
            shutil.copy(
                str(self.source_paths.get(segment_name)),
                str(self.destination_paths.get(segment_name))
            )
    
    def process_for_ffa(self):
        # use lame?
        # add date informtion to file name
        source_file = self.source_paths.get('promo')
        ffa_file_name = f'{self.__class__.__name__} PROMO{source_file.suffix}'
        shutil.copy(
            str(source_file),
            str(self.FOR_FFA.joinpath(ffa_file_name))
        )

    def get_destination_paths(self):
        return {
            segment: self.get_dropbox_file_name(segment, extension=file_path.suffix)
            for segment, file_path in self.source_paths.items()
        }

    def get_dropbox_file_name(self, segment_name, extension='.wav'):
        segment_string = segment_name.replace('_', ' ').upper()

        return self.FOR_DROPBOX.joinpath(
            f'{self.CUT_NUMBERS.get(segment_name)}_{self.__class__.__name__} {segment_string}{extension}'
            )
    
    def get_file_list(self):
        return [
            file_path for file_path in self.LOCAL_PATH.iterdir()
            if self.match_show(file_path.name)
            ]
 
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
            self.SEGEMENT_MATCHES.get(match_string): file_path
            for file_path in self.file_list
            for match_string in self.SEGEMENT_MATCHES.keys() if match_string in file_path.name
        }
    
    def __str__(self):
        return f'-----{self.__class__.__name__}-----\n' + str(self.source_paths)
            
