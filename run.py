# from modules.verify import check_hashes, check_segments
from modules.settings import Execution_Flags, RESET_DIRS
import shutil
from modules.coordinate import Pipe_Control, Sat_Control
from modules.verify import check_segments, check_hashes
from modules.logger import initialize_logger, start_run, close_logger
from modules.copy import copy_all
from modules.check import check_all, slack_check
import pytest


def main():

    if Execution_Flags.TESTS:
        pytest.main(['-vv'])
        return

    if Execution_Flags.SAT:
        Sat_Control(
            process_only=Execution_Flags.PROCESS_ONLY,
            threading=Execution_Flags.THREAD,
            dry_run=Execution_Flags.DRY_RUN
        ).execute()
        return

    if Execution_Flags.RESET:
        remove_directories()
        return
    
    if Execution_Flags.CLEAN:
        clean_directories()
        return

    if Execution_Flags.COPY:
        copy_all()
        return

    if Execution_Flags.CHECK:
        check_all()
        return
    
    if Execution_Flags.VERIFY:
        check_hashes()
        check_segments()
        return
    
    if Execution_Flags.SLACK:
        slack_check()
        return

    Pipe_Control(
        process_only=Execution_Flags.PROCESS_ONLY,
        threading=Execution_Flags.THREAD,
        dry_run=Execution_Flags.DRY_RUN
        ).execute()


def remove_directories():
    logger = initialize_logger('RESET')
    start_run(logger)
    logger.info('Removing audio file directories')

    for directory in RESET_DIRS:
        shutil.rmtree(str(directory), ignore_errors=True)
        print('deleting', directory)
    close_logger(logger)


def clean_directories():
    """ removes non-mp3 and non-wav files created when checking things in 
    Adobe Audition.
    """
    for directory in RESET_DIRS:
        for path in directory.iterdir():
            if path.suffix not in ['.wav', '.mp3', '.json']:
                try:
                    path.unlink(missing_ok=True)
                except IsADirectoryError:
                    # This is just for fake_ffa_mount directory
                    # which contains another directory
                    pass


if __name__ == '__main__':
    main()
