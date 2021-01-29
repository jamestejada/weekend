from modules.settings import (
    THREAD, PROCESS_ONLY, RESET, RESET_DIRS, CLEAN, DRY_RUN,
    FFA_PATH, DROPBOX_PATH, COPY
    )
import shutil
from modules.coordinate import Pipe_Control
from modules.copy import copy_all


# TO DO: 
#   DONE - Add 'reset' functionality to delete directories
#   DONE - Add Air Date to file names
#   DONE - Tweak Latino USA
#   DONE - Add functionality to get latest file if it is newer than stored file.
#   - Add thing to check what files we have and which we still need
#       - Reveal - 
#       (Green) PROMO
#       (Red) SEGMENT A
#   DONE - Maybe instead of having a chooser toggle between 'latest' and 'old'
#       just edit the _get_day_limit() method to return a time range tuple.
#       e.g. (today-timdelta(days=self.weekday + x), today-timedelta(days=self.weekday + y))


def main():

    if RESET:
        remove_directories()
        return
    
    if CLEAN:
        clean_directories()
        return
    
    if COPY:
        copy_all()
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
    """ removes .pkf files created when checking things in 
    Adobe Audition.
    """
    for directory in RESET_DIRS:
        for path in directory.iterdir():
            if path.suffix == '.pkf':
                path.unlink()



if __name__ == '__main__':
    main()
