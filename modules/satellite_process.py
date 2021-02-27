from modules.process import Process_BASE


""" This module gets promos from satellite to process and
transfer to FFA for continuity producers.
"""

class Process_Satellite_BASE(Process_BASE):
    def process_for_ffa(self, key='promo'):
        super().process_for_ffa(key=key)
        # process then delete source in for_dropbox
        # (it already delivers via satellite)
        self.destination_paths.get(key).unlink(missing_ok=True)


class Ask_Me_Another(Process_Satellite_BASE):
    SHOW_MATCH = ['AskMeA1_']
    NUMBER_OF_SHOW_FILES = 1
    AIR_DAYS = [6]
    SEGMENT_MATCHES = {'SGMT01': 'promo'}
    # Develop something to catch generic promos in segment matches later
    CUT_NUMBERS = {'promo': '17020'}


class Hidden_Brain(Process_Satellite_BASE):
    SHOW_MATCH = ['HiddenB1_']
    NUMBER_OF_SHOW_FILES = 1
    SEGMENT_MATCHES = {'SGMT01': 'promo'}
    CUT_NUMBERS = {'promo': '18120'}


class Wait_Wait(Process_Satellite_BASE):
    SHOW_MATCH = ['WaitWa2_']
    NUMBER_OF_SHOW_FILES = 1
    SEGMENT_MATCHES = {'SGMT02': 'promo'}
    CUT_NUMBERS = {'promo': '25366'}


class WeSun(Process_Satellite_BASE):
    SHOW_MATCH = ['Weeken20_']
    NUMBER_OF_SHOW_FILES = 1
    SEGMENT_MATCHES = {'SGMT01': 'promo'}
    CUT_NUMBERS = {'promo': '25389'}
