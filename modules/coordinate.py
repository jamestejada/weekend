from modules.choose import (
    Chooser,
    Chooser_Snap_Judgment,
    Chooser_TAL,
    Chooser_Latino_USA
    )
from modules.process import (
    Reveal,
    Latino_USA,
    Says_You,
    The_Moth,
    Snap_Judgment,
    This_American_Life
)
from modules.ftp import connect
from colorama import Fore, Style
from modules.download import Download_Files

PIPELINES = {
    'LatinoUS': {
        'show_name': 'Latino USA',
        'chooser': Chooser_Latino_USA,
        'processor': Latino_USA
    },
    'RevealWk': {
        'show_name': 'Reveal',
        'chooser': Chooser,
        'processor': Reveal
    },
    'SaysYou1': {
        'show_name': 'Says You',
        'chooser': Chooser,
        'processor': Says_You
    },
    'SnapJudg': {
        'show_name': 'Snap Judgment',
        'chooser': Chooser_Snap_Judgment,
        'processor': Snap_Judgment
    },
    'THEMOTH': {
        'show_name': 'The Moth',
        'chooser': Chooser,
        'processor': The_Moth
    },
    'ThisAmer': {
        'show_name': 'This American Life',
        'chooser': Chooser_TAL,
        'processor': This_American_Life
    }
}

class Pipe_Control:
    PIPELINES = PIPELINES
    GET_OLDER_FILES = ['RevealWk', 'THEMOTH']

    def __init__(self, process_only=False, threading=False, dry_run=False):
        self.file_process_list = []
        self.process_only = process_only
        self.threading = threading
        self.dry_run = dry_run

    def execute(self):
        if not self.process_only:
            self.download_show_files()
        self.process_files()

    def download_show_files(self):
        prx_server = connect()

        for ftp_dir, pipe_info_dict in self.PIPELINES.items():
            print()
            show_name = pipe_info_dict.get('show_name')
            print(Fore.CYAN, f'-{show_name}-', Style.RESET_ALL)
            self._process_ftp_dir(prx_server, ftp_dir)

        prx_server.close()
    
    def _process_ftp_dir(self, server, ftp_dir):
        file_info_generator = server.mlsd(f'/{ftp_dir}')
        files_to_get = self._choose_files(ftp_dir, file_info_generator)

        download_files = Download_Files(server, ftp_dir, files_to_get)
        download_files.download_all()

    def _choose_files(self, ftp_dir, file_info_generator):
        if ftp_dir not in self.PIPELINES.keys():
            return

        which_file_set = 'old' if ftp_dir in self.GET_OLDER_FILES else 'latest'
        chooser_class = self.PIPELINES.get(ftp_dir).get('chooser')
        chooser = chooser_class(
            file_info_generator=file_info_generator,
            which_file_set=which_file_set,
            dry_run=self.dry_run
            )
        file_get_list = chooser.files_to_get()

        for each_file in file_get_list:
            self.file_process_list.append(each_file)
        return file_get_list

    def process_files(self):
        print()
        print(Fore.YELLOW, 'PROCESSING...', Style.RESET_ALL)

        for _, pipe_info_dict in self.PIPELINES.items():
            print()
            show_class = pipe_info_dict.get('processor')
            show = show_class(threading=self.threading, process_list=self.file_process_list)
            print(Fore.CYAN, f'-{show.show_string}-', Style.RESET_ALL)
            show.process()
