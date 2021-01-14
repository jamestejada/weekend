

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
from datetime import datetime, timedelta


def main():
    prx_server = connect()
    file_info_generator = prx_server.mlsd('/RevealWk')

    chooser = Chooser(file_info_generator, which_file_set='old')

    files_only = chooser.all_files
    print(files_only)

    files_to_get = chooser.files_to_get()
    print(files_to_get)

    prx_server.close()

if __name__ == '__main__':
    main()
