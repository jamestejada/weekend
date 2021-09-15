import requests
# from modules import old_process
from modules import process
from modules.data import PRX_DATA_LIST
from modules.logger import start_run, close_logger, initialize_logger
from modules.settings import SLACK_WEBHOOK, Execution_Flags
from colorama import Style, Fore


class Check(process.Process):
    def check(self, slack_run=False):
        exist_dict = self._which_exist()
        if slack_run:
            return self.send_to_slack(exist_dict)
        print(Fore.CYAN, f'\n-{self.show_string}-', Style.RESET_ALL)
        self.check_print(exist_dict)
    
    def send_to_slack(self, exist_dict):
        show_class_name = self.show_string
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
            for segment_name in self.cut_numbers.keys()
        }


# used in run.py
def check_all():
    for show_data in PRX_DATA_LIST:
        Check(show_data).check()
    print()

# used in run.py
def slack_check():
    logger = initialize_logger('CHECK')
    start_run(logger)


    for show_data in PRX_DATA_LIST:
        missing_segments = Check(show_data).check(slack_run=Execution_Flags.SLACK)
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

    logger.info(f'{show_name} missing files: {missing_list}')

    payload = {
        'show_name': show_name,
        'missing_file_list': ', '.join(missing_list)
    }
    requests.post(SLACK_WEBHOOK, json=payload)
