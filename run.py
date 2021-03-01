from modules import process
from modules.settings import (
    THREAD, PROCESS_ONLY, RESET, RESET_DIRS, CLEAN, DRY_RUN,
    COPY, CHECK, SAT
    )
import shutil
from modules.coordinate import Pipe_Control, Sat_Control
from modules.copy import copy_all
from modules.check import check_all


def main():

    if SAT:
        Sat_Control(
            process_only=PROCESS_ONLY,
            threading=THREAD,
            dry_run=DRY_RUN
        ).execute()
        return

    if RESET:
        remove_directories()
        return
    
    if CLEAN:
        clean_directories()
        return
    
    if COPY:
        copy_all()
        return
    
    if CHECK:
        check_all()
        return

    Pipe_Control(
        process_only=PROCESS_ONLY,
        threading=THREAD,
        dry_run=DRY_RUN
        ).execute()


def remove_directories():
    for directory in RESET_DIRS:
        shutil.rmtree(str(directory), ignore_errors=True)

def clean_directories():
    """ removes non-mp3 and non-wav files created when checking things in 
    Adobe Audition.
    """
    for directory in RESET_DIRS:
        for path in directory.iterdir():
            if path.suffix not in ['.wav', '.mp3']:
                path.unlink()



if __name__ == '__main__':
    main()
