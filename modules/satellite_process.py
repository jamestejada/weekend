from modules.process import Process_BASE


""" This module gets promos from satellite to process and
transfer to FFA for continuity producers.
"""

class Process_Satellite_BASE(Process_BASE):
    # Develop something to catch generic promos in segment matches later

    # override
    def process_for_ffa(self, key='promo'):
        super().process_for_ffa(key=key)
        # process then delete source in for_dropbox
        # (it already delivers via satellite)
        dropbox_file_path = self.destination_paths.get(key)
        if dropbox_file_path:
            # delete dropbox file so it doesn't copy to dropbox.
            # That is already done with depot monitor.
            dropbox_file_path.unlink()

    # override
    def _should_skip(self, destination):
        # Don't skip any...process all satellite files.
        return False


class Its_Been_A_Minute(Process_Satellite_BASE):
    SHOW_MATCH = ['ItsBeen1_']
    NUMBER_OF_SHOW_FILES = 1
    AIR_DAYS = [5]
    SEGMENT_MATCHES = {'SGMT01': 'promo'}
    CUT_NUMBERS = {'promo': '17790'}


class Ask_Me_Another(Process_Satellite_BASE):
    SHOW_MATCH = ['AskMeA1_']
    NUMBER_OF_SHOW_FILES = 1
    AIR_DAYS = [6]
    SEGMENT_MATCHES = {'SGMT01': 'promo'}
    CUT_NUMBERS = {'promo': '17020'}


class Hidden_Brain(Process_Satellite_BASE):
    SHOW_MATCH = ['HiddenB1_']
    NUMBER_OF_SHOW_FILES = 1
    AIR_DAYS = [6]
    SEGMENT_MATCHES = {'SGMT01': 'promo'}
    CUT_NUMBERS = {'promo': '18120'}


class Wait_Wait(Process_Satellite_BASE):
    SHOW_MATCH = ['WaitWa2_']
    NUMBER_OF_SHOW_FILES = 2
    AIR_DAYS = [5, 6]
    SEGMENT_MATCHES = {'SGMT02': 'promo'}
    CUT_NUMBERS = {'promo': '25366'}


class WeSun(Process_Satellite_BASE):
    SHOW_MATCH = ['Weeken20_']
    NUMBER_OF_SHOW_FILES = 1
    AIR_DAYS = [6]
    SEGMENT_MATCHES = {'SGMT01': 'promo'}
    CUT_NUMBERS = {'promo': '25389'}
