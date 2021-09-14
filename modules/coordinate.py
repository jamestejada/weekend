from modules.settings import PATHS
from modules import choose, old_process, satellite_process, verify, process
from modules.ftp import connect
from colorama import Fore, Style
from modules.download import Download_Files, Sat_Download
from modules.logger import initialize_logger, start_run, close_logger

from modules.process import Process
from modules.data import LATINO_USA, REVEAL, SAYS_YOU, SNAP_JUDGMENT, THE_MOTH, THIS_AMERICAN_LIFE
from modules.data import PRX_DATA_LIST, SATELLITE_DATA_LIST


EXECUTIONS = {
    'LatinoUS': {
        'show_name': 'Latino USA',
        'chooser': choose.Chooser_Latino_USA,
        'processor': old_process.Latino_USA,
        'verifier': verify.Segment_Verifier,
        'show_data': LATINO_USA
    },
    'RevealWk': {
        'show_name': 'Reveal',
        'chooser': choose.Chooser_Reveal,
        'processor': old_process.Reveal,
        'verifier': verify.Segment_Verifier,
        'show_data': REVEAL
    },
    'SaysYou1': {
        'show_name': 'Says You',
        'chooser': choose.Chooser,
        'processor': old_process.Says_You,
        'verifier': verify.Segment_Verifier,
        'show_data': SAYS_YOU
    },
    'SnapJudg': {
        'show_name': 'Snap Judgment',
        'chooser': choose.Chooser_Snap_Judgment,
        'processor': old_process.Snap_Judgment,
        'verifier': verify.Segment_Verifier,
        'show_data': SNAP_JUDGMENT
    },
    'THEMOTH': {
        'show_name': 'The Moth',
        'chooser': choose.Chooser,
        'processor': old_process.The_Moth,
        'verifier': verify.Segment_Verifier,
        'show_data': THE_MOTH
    },
    'ThisAmer': {
        'show_name': 'This American Life',
        'chooser': choose.Chooser_TAL,
        'processor': old_process.This_American_Life,
        'verifier': verify.Segment_Verifier,
        'show_data': THIS_AMERICAN_LIFE
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
    SHOW_LIST = PRX_DATA_LIST

    def __init__(self, process_only: bool = False, 
            threading: bool = False, dry_run: bool = False):
        
        self.logger = initialize_logger()
        start_run(self.logger)

        self.show_data_list = self.SHOW_LIST
        self.file_process_list = []
        self.process_only = process_only
        self.threading = threading
        self.dry_run = dry_run

        self.hash_verifier = verify.Hash_Verifier
        self.segment_verifer = verify.Segment_Verifier

        self.logger.info(f'PROCESS ONLY: {self.process_only}')
        self.logger.info(f'THREADING: {self.threading}')
        self.logger.info(f'DRY RUN: {self.dry_run}')

        for var, value in self.__dict__.items():
            self.logger.debug(f'{var}: {value}')

    # main
    def execute(self):
        # try:
        if not self.process_only:
            self.download_show_files()
        self.logger.info(f'Files to be Processed: {self.file_process_list}')
        self.process_files()
        # except Exception as e:
        #     print(e)
        #     self.logger.warn(f'EXCEPTION: {e.__class__.__name__} - {e}')
        # finally:
        #     close_logger(self.logger)

    def download_show_files(self):

        prx_server = connect()

        message_level = self.logger.info if prx_server else self.logger.warn
        message = 'Connected to FTP' if prx_server else 'Connection could not be established'
        message_level(message)

        # for ftp_dir, pipe_info_dict in self.EXECUTIONS.items():
        for show_data in self.show_data_list:
            print(f'Checking {show_data.remote_dir} on PRX server', end="\r")
            self._process_ftp_dir(prx_server, show_data)
            print(' '*40, end='\r')

        if prx_server:
            prx_server.close()
            self.logger.info('Connection to FTP closed')
    
    def _process_ftp_dir(self, server, show_data):
        verifier = self.hash_verifier(
            server, show_data.remote_dir, match_list=show_data.show_match
            )
        corrupted_files = verifier.check_hashes()
        file_info_generator = server.mlsd(f'/{show_data.remote_dir}')

        if corrupted_files:
            self.logger.warn(
                f'CORRUPTED FILES TO BE RE-DOWNLOADED: {corrupted_files}'
                )

        files_to_get = [
            *self._choose_files(show_data, file_info_generator),
            *corrupted_files
            ]

        self.logger.info(
            f'Chosen Files from FTP for {show_data.show_name}: {files_to_get}'
            )

        if files_to_get:
            self.print_show(show_data.show_name)

        download_files = Download_Files(server, show_data.remote_dir, files_to_get)
        download_files.download_all()
    
    def print_show(self, show_name):
        print(' '*40, end='\r')
        print(Fore.CYAN, f'-{show_name}-', Style.RESET_ALL)

    def _choose_files(self, show_data, file_info_generator):

        which_file_set = 'old' if show_data.remote_dir in self.GET_OLDER_FILES else 'latest'
        chooser_class = self.EXECUTIONS.get(show_data.remote_dir).get('chooser')
        path_list = Process(show_data).file_list
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
        self._print_processing_message()
        for show_data in self.show_data_list:
            self.print_show(show_data.show_name)
            self._process_one_show(show_data=show_data)
            self._verify_processed_files(show_data=show_data)

    def _print_processing_message(self):
        print()
        print(Fore.YELLOW, 'PROCESSING...', Style.RESET_ALL)

    def _process_one_show(self, show_data, any_file_mistimed=False):
        """Instantiates a processor class and runs the process() method"""
        process_list = None if any_file_mistimed else self.file_process_list
        print(process_list)
        Process(
            show_data=show_data,
            process_list=process_list,
            threading=self.threading,
            force=self.process_only
            ).process()

    def _verify_processed_files(self, show_data:object) -> None:
        """Verifies processed file lengths. If any processed files are not the correct
        length, the files are deleted and reprocessed. 
        """
        # length_verifier_class = pipe_info.get('verifier')
        mistimed_files = verify.Segment_Verifier(show_data).verify_show()
        if mistimed_files:
            self._delete_bad_files(mistimed_files)
            self.logger.warn('Retrying processing')
            self._process_one_show(show_data, any_file_mistimed=True)

    def _delete_bad_files(self, bad_files: list) -> None:
        for bad_file in bad_files:
            self.logger.warn(f'{bad_file.name} is not timed correctly and will be removed.')
            bad_file.unlink()


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
            file_path.name for file_path in PATHS.SAT_PATH.iterdir()
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
        for file_path in PATHS.SAT_PATH.iterdir():
            file_path.unlink()
