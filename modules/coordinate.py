from os import close, pipe
from typing import final
from modules import download
from modules.settings import SAT_PATH
from modules import choose, process, satellite_process
from modules.ftp import connect
from colorama import Fore, Style
from modules.download import Download_Files, Sat_Download
from modules.logger import initialize_logger, start_run, close_logger


EXECUTIONS = {
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

SAT_EXEC = {
    'Its_Been_A_Minute':{
        'show_name': 'Its Been a Minute',
        'processor': satellite_process.Its_Been_A_Minute
    },
    'Ask_Me_Another': {
        'show_name': 'Ask Me Another',
        'processor': satellite_process.Ask_Me_Another
    },
    'Hidden_Brain': {
        'show_name': 'Hidden Brain',
        'processor': satellite_process.Hidden_Brain
    },
    'Wait_Wait': {
        'show_name': 'Wait Wait... Don\'t Tell Me!',
        'processor': satellite_process.Wait_Wait
    },
    'WeSun': {
        'show_name': 'Weekend Edition Sunday',
        'processor': satellite_process.WeSun
    }
}


class Pipe_Control:
    """This class coordinates choosing, downloading and processing
    of various show files."""
    EXECUTIONS = EXECUTIONS
    GET_OLDER_FILES = ['RevealWk', 'THEMOTH']

    def __init__(self, process_only: bool = False, 
            threading: bool = False, dry_run: bool = False):
        
        self.logger = initialize_logger()
        start_run(self.logger)

        self.file_process_list = []
        self.process_only = process_only
        self.threading = threading
        self.dry_run = dry_run
        self.logger.info(f'PROCESS ONLY: {self.process_only}')
        self.logger.info(f'THREADING: {self.threading}')
        self.logger.info(f'DRY RUN: {self.dry_run}')

        for var, value in self.__dict__.items():
            self.logger.debug(f'{var}: {value}')

    # main
    def execute(self):
        try:
            if not self.process_only:
                self.download_show_files()
            self.process_files()
        except Exception as e:
            self.logger.warn(f'EXCEPTION: {e.__class__.__name__} - {e}')
        finally:
            close_logger(self.logger)

    def download_show_files(self):
        prx_server = connect()
        
        if prx_server:
            self.logger.info('Connected to FTP')
        else:
            self.logger.warn('Connection could not be established')

        for ftp_dir, pipe_info_dict in self.EXECUTIONS.items():
            print(f'Checking {ftp_dir} on PRX server', end="\r")
            self._process_ftp_dir(prx_server, ftp_dir, pipe_info_dict)
            print(' '*40, end='\r')

        if prx_server:
            self.logger.info('Connection to FTP closed')
        prx_server.close()
    
    def _process_ftp_dir(self, server, ftp_dir, pipe_info):
        file_info_generator = server.mlsd(f'/{ftp_dir}')
        files_to_get = self._choose_files(ftp_dir, file_info_generator)

        self.logger.info(
            f'Chosen Files from FTP for {pipe_info.get("show_name")}: {files_to_get}'
            )

        if files_to_get:
            self.print_show(pipe_info.get('show_name'))

        download_files = Download_Files(server, ftp_dir, files_to_get)
        download_files.download_all()
    
    def print_show(self, show_name):
        print()
        print(Fore.CYAN, f'-{show_name}-', Style.RESET_ALL)

    def _choose_files(self, ftp_dir, file_info_generator):
        if ftp_dir not in self.EXECUTIONS.keys():
            return

        which_file_set = 'old' if ftp_dir in self.GET_OLDER_FILES else 'latest'
        chooser_class = self.EXECUTIONS.get(ftp_dir).get('chooser')

        # for getting local files of same show
        process_class = self.EXECUTIONS.get(ftp_dir).get('processor')
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

        for _, pipe_info_dict in self.EXECUTIONS.items():
            self.print_show(pipe_info_dict.get('show_name'))
            show_class = pipe_info_dict.get('processor')
            show = show_class(
                threading=self.threading, process_list=self.file_process_list
                )
            show.process()


class Sat_Control:
    SAT_EXEC = SAT_EXEC

    def __init__(self, process_only: bool = False, 
            threading: bool = False, dry_run: bool = False):

        self.logger = initialize_logger('SATELLITE')
        start_run(self.logger)

        self.process_only = process_only
        self.threading = threading
        self.dry_run = dry_run

        for var, value in self.__dict__.items():
            self.logger.debug(f'{var}: {value}')

    def execute(self):
        self.download_show_files()
        self.process()
        close_logger(self.logger)

    def download_show_files(self):
        print()
        print(
            Fore.YELLOW,
            'DOWNLOADING from XDS Satellite Receiver...',
            Style.RESET_ALL
            )
        all_results = []
        for _, pipe_info in self.SAT_EXEC.items():
            download_list = self._choose_files(pipe_info)

            self.logger.info(f'{pipe_info.get("show_name")} Download List: {download_list}')

            if download_list:
                self.print_show(pipe_info.get('show_name'))

            download_files = Sat_Download(download_list=download_list)
            one_show_results = download_files.download_all()

            self.logger.debug(
                f'Download results for {pipe_info.get("show_name")}: {one_show_results}'
                )

            all_results.append(one_show_results)
        
        if self._all_success(all_results):
            self.logger.info(f'All Downloads Suceed? {self._all_success(all_results)}')
            self.clear_satellite()
    
    def _all_success(self, results: list):
        """ checks all sublists of results list
        for any False values (if a copy command fails)
        """
        return all(
            [all(result) for result in results]
        )

    def _choose_files(self, pipe_info: dict):
        processor = self._get_processor_instance(pipe_info)
        return [
            file_path.name for file_path in SAT_PATH.iterdir()
            if processor.match_show(file_path.stem)
        ]

    def process(self):
        print()
        print(Fore.YELLOW, 'PROCESSING...', Style.RESET_ALL)

        for _, pipe_info in self.SAT_EXEC.items():
            show_name = pipe_info.get('show_name')
            self.print_show(show_name)
            processor = self._get_processor_instance(pipe_info)
            processor.process()
        print()
    
    def _get_processor_instance(self, pipe_info: dict):
        processor_class = pipe_info.get('processor')
        return processor_class()
    
    def print_show(self, show_name):
        print()
        print(Fore.CYAN, f'-{show_name}-', Style.RESET_ALL)
    
    def clear_satellite(self):
        print(Fore.RED, 'Deleting all files from Sat Receiver...', Style.RESET_ALL)
        self.logger.info('Deleting all files from Sat Receiver')
        for file_path in SAT_PATH.iterdir():
            file_path.unlink()
