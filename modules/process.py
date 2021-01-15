from modules.settings import LOCAL_PATH


class Reveal:
    SHOW_MATCH = ['RevealWk_']
    PROMO_MATCH = 'PROM01'
    BILL_BOARD_MATCH = 'SGMT01'
    MUSIC_BEDS = [
        'SGMT02',
        'SGMT04',
        'SGMT06'
    ]
    SEGMENT_A = 'SGMT03'
    SEGMENT_B = 'SGMT05'
    SEGMENT_C = 'SGMT07'

    LOCAL_PATH = LOCAL_PATH
    
    def __init__(self):
        self.file_list = self.get_file_list()
    
    def get_file_list(self, _target_dir=None):
        target_dir = _target_dir or self.LOCAL_PATH
        return [
            file_path.name for file_path in target_dir.iterdir()
            if self.match_show(file_path.name)
            ]
 
    def match_show(self, file_name):
        return any((show_match_str in file_name) for show_match_str in self.SHOW_MATCH)


    # def process(self, )