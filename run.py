# TO DO: 
#   - Add mp3 conversion for FFA promos?
#       - or just user audition (this would also take
#           care of loudness standards etc.)

from modules.ftp import download_show_files
from modules.process import process_all
from modules.settings import PROCESS_ONLY, RESET, RESET_DIRS
import shutil


# TO DO: 
#   DONE - Add 'reset' functionality to delete directories
#   DONE - Add Air Date to file names
#   - Maybe instead of having a chooser toggle between 'latest' and 'old'
#       just edit the _get_day_limit() method to return a time range tuple.
#       e.g. (today-timdelta(days=self.weekday + x), today-timedelta(days=self.weekday + y))


import time
def main():

    if RESET:
        for directory in RESET_DIRS:
            shutil.rmtree(str(directory), ignore_errors=True)
        return

    if not PROCESS_ONLY:
        download_show_files()

    start = time.perf_counter()
    process_all()
    end = time.perf_counter()

    thread_start = time.perf_counter()
    process_all(threading=True)
    thread_end = time.perf_counter()

    print(f'non-threading processing time: {end - start}')
    print(f'threading processing time: {thread_end - thread_start}')


if __name__ == '__main__':
    main()
