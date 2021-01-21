# TO DO: 
#   - Add mp3 conversion for FFA promos?
#       - or just user audition (this would also take
#           care of loudness standards etc.)

from modules.ftp import download_show_files
from modules.process import process_all
from modules.settings import PROCESS_ONLY, RESET, RESET_DIRS
import shutil


from modules.process import PROGRAM_LIST


# TO DO: 
#   DONE - Add 'reset' functionality to delete directories
#   - Add Air Date to file names
def main():

    if RESET:
        for directory in RESET_DIRS:
            shutil.rmtree(str(directory), ignore_errors=True)
        return

    prx_server = None
    if not PROCESS_ONLY:
        download_show_files()

    process_all()


if __name__ == '__main__':
    main()
