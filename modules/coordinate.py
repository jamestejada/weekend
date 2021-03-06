from modules.settings import PATHS
from modules import choose, verify, process, satellite_process
from modules.ftp import connect
from colorama import Fore, Style
from modules.download import Download_Files, Sat_Download
from modules.logger import initialize_logger, start_run, close_logger

from modules.data import PRX_DATA_LIST, SATELLITE_DATA_LIST



class Pipe_Control:
    """This class coordinates choosing, downloading and processing
    of various show files."""
    GET_OLDER_FILES = ['RevealWk', 'THEMOTH', 'TheChamb']
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
        self.processor = process.Process
        self.chooser = choose.Chooser

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
            self.logger.info(f'Files to be Processed: {self.file_process_list}')
            self.process_files()
        except Exception as e:
            print(e)
            self.logger.warn(f'EXCEPTION: {e.__class__.__name__} - {e}')
        finally:
            close_logger(self.logger)

    def download_show_files(self):

        prx_server = connect()

        message_level = self.logger.info if prx_server else self.logger.warn
        message = 'Connected to FTP' if prx_server else 'Connection could not be established'
        message_level(message)

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
        path_list = self.processor(show_data).file_list
        local_list = [file_path.name for file_path in path_list]

        file_get_list = self.chooser(
                file_info_generator=file_info_generator,
                which_file_set=which_file_set,
                local_list=local_list,
                dry_run=self.dry_run,
                first_day_offset_offset=show_data.first_day_offset_offset
            ).files_to_get()

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
        self.processor(
            show_data=show_data,
            process_list=process_list,
            threading=self.threading,
            force=self.process_only
            ).process()

    def _verify_processed_files(self, show_data:object) -> None:
        """Verifies processed file lengths. If any processed files are not the correct
        length, the files are deleted and reprocessed. 
        """
        mistimed_files = self.segment_verifer(show_data).verify_show()
        if mistimed_files:
            self._delete_bad_files(mistimed_files)
            self.logger.warn('Retrying processing')
            self._process_one_show(show_data, any_file_mistimed=True)

    def _delete_bad_files(self, bad_files: list) -> None:
        for bad_file in bad_files:
            self.logger.warn(f'{bad_file.name} is not timed correctly and will be removed.')
            bad_file.unlink()


class Sat_Control:
    SHOW_LIST = SATELLITE_DATA_LIST

    def __init__(self, process_only: bool = False, 
            threading: bool = False, dry_run: bool = False):

        self.logger = initialize_logger('SATELLITE')
        start_run(self.logger)

        self.process_only = process_only
        self.threading = threading
        self.dry_run = dry_run

        self.processor = satellite_process.Process_Satellite

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
        for show_data in self.SHOW_LIST:
            download_list = self._choose_files(show_data)
            self.logger.info(f'{show_data.show_name} Download List: {download_list}')

            if download_list:
                self.print_show(show_data.show_name)
            
            download_files = Sat_Download(download_list=download_list)
            one_show_result = download_files.download_all()

            self.logger.debug(
                f'Download results for {show_data.show_name}: {one_show_result}'
            )
            
            all_results.append(one_show_result)
        
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

    def _choose_files(self, show_data:object):
        processor = self.processor(show_data)
        return [
            file_path.name for file_path in PATHS.SAT_PATH.iterdir()
            if processor.match_show(file_path.stem)
        ]

    def process(self):
        print(Fore.YELLOW, '\nPROCESSING...', Style.RESET_ALL)
        for show_data in self.SHOW_LIST:
            self.print_show(show_data.show_name)
            self.processor(show_data).process()
        print()
    
    def print_show(self, show_name):
        print(Fore.CYAN, f'\n-{show_name}-', Style.RESET_ALL)
    
    def clear_satellite(self):
        print(Fore.RED, 'Deleting all files from Sat Receiver...', Style.RESET_ALL)
        self.logger.info('Deleting all files from Sat Receiver')
        for file_path in PATHS.SAT_PATH.iterdir():
            file_path.unlink()
