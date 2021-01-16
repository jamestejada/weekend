

# 1. Get File
#   a. log in to ftp or scrape to get download link 
#   b. determine which program to download (maybe by modified date)
#   c. Download file

# ???: start here. Process files from a "dump" folder.
# 2. process file
#   a. create mp3 version of promo
#       - ***lame.exe?
#       - mutagen?
#   b. rename .wav for ingest into DAD
#       - cut number
#       - title
#       - etc

# 3. copy to destinations
#   a. DAD DROPBOX
#   b. FFA Continuity Folder.

# NOTE: This is a reminder to redo files_to_get() method in
#       Chooser Class. Make it so that it groups week by Monday - Sunday
#       or something like that. 

from modules.ftp import connect
from modules.choose import Chooser
from modules.download import Download_Files
from modules.settings import LOCAL_PATH, PROCESS_ONLY
from datetime import datetime, timedelta


from modules.process import Reveal

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

    show = Reveal()
    print(show)
    show.process()
    print(show.destination_paths)

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
