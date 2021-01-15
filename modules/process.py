from modules.settings import LOCAL_PATH


class Reveal:
    SHOW_MATCH = ['RevealWk_']
    PROMO_MATCH = 'PROM01'
    SEGEMENT_MATCHES = {
        'SGMT01': 'billboard',
        'SGMT03': 'segment_a',
        'SGMT05': 'segment_b',
        'SGMT07': 'segment_c'
    }
    MUSIC_BEDS = {
        'SGMT02': 'music_a',
        'SGMT04': 'music_b',
        'SGMT06': 'music_c'
    }
    LOCAL_PATH = LOCAL_PATH
    
    def __init__(self):
        self.file_list = self.get_file_list()
        self.segment_info_dict = self.get_segment_info()
    
    def get_file_list(self, ):
        return [
            file_path for file_path in self.LOCAL_PATH.iterdir()
            if self.match_show(file_path.name)
            ]
 
    def match_show(self, file_name):
        return any((show_match_str in file_name) for show_match_str in self.SHOW_MATCH)
    
    def get_segment_info(self):
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
        return f'-----{self.__class__.__name__}-----\n' + str(self.segment_info_dict)
            
