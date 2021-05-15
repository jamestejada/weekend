import requests
from modules import process
from modules.logger import start_run, close_logger, initialize_logger
from modules.settings import SLACK, SLACK_WEBHOOK
from colorama import Style, Fore


class Check_BASE(process.Process_BASE):
    def check(self, slack_run=False):
        exist_dict = self._which_exist()
        if slack_run:
            return self.send_to_slack(exist_dict)
        print(Fore.CYAN, f'\n-{self}-', Style.RESET_ALL)
        self.check_print(exist_dict)
    
    def send_to_slack(self, exist_dict):
        show_class_name = self.__class__.__name__
        missing_segments = {
            show_class_name: [
                segment.replace('_', ' ').title() 
                for segment in exist_dict if not exist_dict.get(segment)
                ]
            }
        if len(missing_segments.get(show_class_name)) > 0:
            return missing_segments

    def check_print(self, exist_dict):
        for segment, exist in exist_dict.items():
            color, style = (Fore.GREEN, Style.BRIGHT) if exist else (Fore.RED, Style.DIM)
            print(color, style, segment.replace('_', ' ').title(), Style.RESET_ALL)

    
    def _which_exist(self):
        """ Compares set of all possible segments to existing segments
        in download folder and creates a dictionary with booleans for each
        possible segment.
        """
        return {
            segment_name: (segment_name in self.source_paths.keys())
            for segment_name in self.CUT_NUMBERS.keys()
        }
    
    def __str__(self):
        return self.__class__.__name__.replace('_', ' ')

# NOTE: Check_BASE inherits from Process_BASE, and then the 
#       show checking classes below inherit from the show processing
#       classes, which inherit from Process_BASE also. 
# TO DO: test if you don't need to inherit from process.Process_BASE.
class Reveal(Check_BASE, process.Reveal): ...
class Latino_USA(Check_BASE, process.Latino_USA): ...
class Says_You(Check_BASE, process.Says_You): ...
class The_Moth(Check_BASE, process.The_Moth): ...
class Snap_Judgment(Check_BASE, process.Snap_Judgment): ...
class This_American_Life(Check_BASE, process.This_American_Life): ...


CHECK_SHOWS = [
    Reveal, 
    Latino_USA,
    Says_You,
    The_Moth,
    Snap_Judgment,
    This_American_Life
]

# used in run.py
def check_all():
    for show_class in CHECK_SHOWS:
        show = show_class()
        show.check()
    print()

# used in run.py
def slack_check():
    logger = initialize_logger('CHECK')
    start_run(logger)

    for show_class in CHECK_SHOWS:
        show = show_class()
        missing_segments = show.check(slack_run=SLACK)
        if missing_segments:
            request_handler(missing_segments, logger=logger)

    close_logger(logger)

def request_handler(missing_segment_dict: dict, logger=None):
    """ missing_segment_dict should be of form:
        {
            'This_American_Life': [
                segment_a,
                music_bed_a,
                segment_b
            ]
        }
    """
    show_name = list(missing_segment_dict.keys())[0]
    missing_list = missing_segment_dict.get(show_name)

    logger.info(f'{show_name.replace("_", " ")} missing files: {missing_list}')

    payload = {
        'show_name': show_name.replace('_', ' '),
        'missing_file_list': ', '.join(missing_list)
    }
    requests.post(SLACK_WEBHOOK, json=payload)