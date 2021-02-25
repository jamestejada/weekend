from modules import choose, process
from modules.ftp import connect
from colorama import Fore, Style
from modules.download import Download_Files

PIPELINES = {
    'LatinoUS': {
        'show_name': 'Latino USA',
        'chooser': choose.Chooser_Latino_USA,
        'processor': process.Latino_USA
    },
    'RevealWk': {
        'show_name': 'Reveal',
        'chooser': choose.Chooser_Reveal,
        'processor': process.Reveal
    },
    'SaysYou1': {
        'show_name': 'Says You',
        'chooser': choose.Chooser,
        'processor': process.Says_You
    },
    'SnapJudg': {
        'show_name': 'Snap Judgment',
        'chooser': choose.Chooser_Snap_Judgment,
        'processor': process.Snap_Judgment
    },
    'THEMOTH': {
        'show_name': 'The Moth',
        'chooser': choose.Chooser,
        'processor': process.The_Moth
    },
    'ThisAmer': {
        'show_name': 'This American Life',
        'chooser': choose.Chooser_TAL,
        'processor': process.This_American_Life
    }
}

class Pipe_Control:
    """This class coordinates choosing, downloading and processing
    of various show files."""
    PIPELINES = PIPELINES
    GET_OLDER_FILES = ['RevealWk', 'THEMOTH']

    def __init__(self, process_only=False, threading=False, dry_run=False):
        self.file_process_list = []
        self.process_only = process_only
        self.threading = threading
        self.dry_run = dry_run

    # main
    def execute(self):
        if not self.process_only:
            self.download_show_files()
        self.process_files()

    def download_show_files(self):
        prx_server = connect()

        for ftp_dir, pipe_info_dict in self.PIPELINES.items():
            self._process_ftp_dir(prx_server, ftp_dir, pipe_info_dict)

        prx_server.close()
    
    def _process_ftp_dir(self, server, ftp_dir, pipe_info):
        file_info_generator = server.mlsd(f'/{ftp_dir}')
        files_to_get = self._choose_files(ftp_dir, file_info_generator)

        if files_to_get:
            self.print_show(pipe_info.get('show_name'))

        download_files = Download_Files(server, ftp_dir, files_to_get)
        download_files.download_all()
    
    def print_show(self, show_name):
        print()
        print(Fore.CYAN, f'-{show_name}-', Style.RESET_ALL)


    def _choose_files(self, ftp_dir, file_info_generator):
        if ftp_dir not in self.PIPELINES.keys():
            return

        which_file_set = 'old' if ftp_dir in self.GET_OLDER_FILES else 'latest'
        chooser_class = self.PIPELINES.get(ftp_dir).get('chooser')

        # for getting local files of same show
        process_class = self.PIPELINES.get(ftp_dir).get('processor')
        path_list = process_class().get_file_list()
        local_list = [file_path.name for file_path in path_list]

        chooser = chooser_class(
                file_info_generator=file_info_generator,
                which_file_set=which_file_set,
                local_list=local_list,
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
            self.print_show(pipe_info_dict.get('show_name'))
            show_class = pipe_info_dict.get('processor')
            show = show_class(threading=self.threading, process_list=self.file_process_list)
            show.process()
