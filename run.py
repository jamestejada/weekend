# TO DO: 
#   - Add mp3 conversion for FFA promos?
#       - or just user audition (this would also take
#           care of loudness standards etc.)

from modules.ftp import download_show_files
from modules.process import process_all
from modules.settings import THREAD, PROCESS_ONLY, RESET, RESET_DIRS
import shutil


# TO DO: 
#   DONE - Add 'reset' functionality to delete directories
#   DONE - Add Air Date to file names
#   - Tweak Latino USA
#   - Add functionality to get latest file if it is newer than stored file.
#   - Add thing to check what files we have and which we still need
#       - Reveal - 
#       (Green) PROMO
#       (Red) SEGMENT A
#   DONE - Maybe instead of having a chooser toggle between 'latest' and 'old'
#       just edit the _get_day_limit() method to return a time range tuple.
#       e.g. (today-timdelta(days=self.weekday + x), today-timedelta(days=self.weekday + y))


import time
def main():

    if RESET:
        remove_directories()
        return

    if not PROCESS_ONLY:
        download_show_files()

    process_all(threading=THREAD)


def remove_directories():
    for directory in RESET_DIRS:
        shutil.rmtree(str(directory), ignore_errors=True)


if __name__ == '__main__':
    main()
