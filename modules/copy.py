from modules.logger import initialize_logger, start_run, close_logger
from modules.settings import FFA_PATH, DROPBOX_PATH, FOR_FFA, FOR_DROPBOX
from modules.choose import Chooser
from colorama import Fore, Style
import shutil
from datetime import datetime, timedelta


def copy_all():
    logger = initialize_logger('COPY')
    start_run(logger)

    for each_file in FOR_FFA.iterdir():
        modified_date = each_file.stat().st_mtime
        modified_date_str = datetime.fromtimestamp(modified_date).strftime('%Y%m%d%H%M%S')


        static_chooser = Chooser()
        should_upload = static_chooser.date_compare(
                    modified_date_str
                ) and static_chooser.is_newer(
                    each_file.name,
                    modified_date_str,
                    local_file_dir=FFA_PATH
                )
        
        logger.debug(f'File: {each_file.name} modified {modified_date_str}')
        logger.debug(f'Should Upload? {should_upload}')
        
        if should_upload and each_file.suffix in ['.mp3', '.wav']:
            print(f'Copying {each_file.name} from {each_file.parent.stem} to FFA')
            try:
                shutil.copyfile(
                    str(each_file),
                    str(FFA_PATH.joinpath(each_file.name))
                )
            except Exception as e:
                print(Fore.RED, Style.BRIGHT, 'COPY ERROR: ', e, Style.RESET_ALL)
                logger.warn(f'COPY FAILED: {e.__class__.__name__} - {e}')

    for each_file in FOR_DROPBOX.iterdir():
        modified_date = datetime.fromtimestamp(each_file.stat().st_mtime)
        now = datetime.now()
        max_time = timedelta(minutes=120)

        should_upload = all([
            ((now - modified_date) < max_time),
            each_file.suffix in ['.mp3', '.wav'],
            ])

        logger.debug(f'File: {each_file.name} modified {modified_date.strftime("%Y%m%d%H%M%S")}')
        logger.debug(f'Should Upload? {should_upload}')

        if should_upload:
            print(f'Copying {each_file.name} from {each_file.parent.stem} to DROPBOX')
            try:
                shutil.copyfile(
                    str(each_file),
                    str(DROPBOX_PATH.joinpath(each_file.name))
                )
            except Exception as e:
                print(Fore.RED, Style.BRIGHT, 'COPY ERROR: ', e, Style.RESET_ALL)
                logger.warn(f'COPY FAILED: {e.__class__.__name__} - {e}')

    close_logger(logger)




