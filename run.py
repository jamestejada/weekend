# TO DO: 
#   - Add mp3 conversion for FFA promos?
#       - or just user audition (this would also take
#           care of loudness standards etc.)

 

from modules.ftp import connect
from modules.choose import Chooser
from modules.download import Download_Files
from modules.settings import LOCAL_PATH, PROCESS_ONLY
from datetime import datetime, timedelta


from modules.process import PROGRAM_LIST

dir_list = [
    'LatinoUS',
    'RevealWk',
    'SaysYou1',
    'SnapJudg',
    'THEMOTH',
    'ThisAmer'
]



def main():
    prx_server = None

    if not PROCESS_ONLY:
        prx_server = connect()

        for directory in dir_list:
            process_dir(prx_server, directory)

    for program_class in PROGRAM_LIST:
        show = program_class()
        # print(show.source_paths)
        show.process()
        # print(show.destination_paths)

    if prx_server:
        prx_server.close()



def process_dir(prx_server, directory):
    
    print(f'---------{directory}---------')
    which_file_set = 'old' if directory == 'RevealWk' else 'latest'

    file_info_generator = prx_server.mlsd(f'/{directory}')

    chooser = Chooser(file_info_generator, which_file_set=which_file_set)

    # files_only = chooser.all_files
    # print(files_only)

    files_to_get = chooser.files_to_get()
    # print(files_to_get)

    download_files = Download_Files(prx_server, directory, files_to_get)
    download_files.download_all()


if __name__ == '__main__':
    main()
