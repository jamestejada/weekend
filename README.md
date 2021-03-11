# CapRadio Weekend Programming Bot

## The Original 'Manual' Process
1. Download show files from PRX as they appear (this requires checking the ftp at regular intervals)
1. Normalize to -24 LUFs
1. Rename files for Dropbox
    - EXAMPLE: `14160_Snap Judgment SEGMENT C Mar 7.wav`
1. Convert to mp3 (only needed for promos used for remote continuity)
1. Rename for remote continuity folder on network drive (i.e. promos used by remote hosts during breaks)
    - EXAMPLE: `This American Life PROMO Mar 6 and Mar 7.mp3`
1. Copy files to their appropriate destinations (ENCO Dropbox, or remote continuity folder)
1. BONUS TASK A: Get satellite files for show promos so that remote hosts can use those as well.
1. BONUS TASK B: Delete satellite files off of the backup receiver (this is so that we can keep a "hot" backup of our satellite receiver configured in the exact same way as the primary without overloading the harddrive on the receiver)

## What does this program do?
All of the above, but **automatically**.

## Features
- Automatic file downloads
    - Based on modified date as well as episode number
    - Satellite files are downloaded as well
- Renaming of files based on air date.
- Automatic renames files with the correct names based on air date
- Automatic processing of files
    - Normalization to industry standard (-24 LUFs)
    - mp3 conversion for promos
- Copying files appropriate destinations (i.e. ENCO Dropbox, or Continuity Folder)
- Deletes files from satellite receiver
- Threading (well... Python 'threading') for increased audio processing speed. (Threading allows the execution of multiple processes at the same time)

## Requirements
### Development Environment
- Python 3.8.5
- Ubuntu 20.04 LTS Server (As OS or Windows Subsystem for Linux Distrubution)

### Dependencies
- [ffmpeg](https://ffmpeg.org/) for audio processing
- [cifs-utils](https://wiki.samba.org/index.php/LinuxCIFS_utils) (not needed on WSL) - Used for mounting Windows network drives from linux
- libraries:
    - python-dotenv
    - ffmpeg-normalize

## Setup
1. Clone repository (currently private)
1. Create a `.env` file in the modules folder with the following fields (NOTE: Do not use quotes around the paths)
    - Mount paths
        - `SAT_MOUNT={{ satellite samba mount path }}`
        - `DROPBOX_MOUNT={{ Dropbox samba mount path }}`
        - `FFA_MOUNT={{ remote continuity mount path }}`
        - EXAMPLE: 
            ```
            DROPBOX_MOUNT=/mnt/dropbox
            ```
    - PRX FTP credentials
        - `PRX_IP={{ IP Address }}`
        - `PRX_USERNAME={{ username }}`
        - `PRX_PASSWORD={{ password }}`
1. Create mount paths for satellite, dropbox, remote-continuity network shares. Make sure they are the same paths you set in the `.env` file.
    - EXAMPLE: 
        ```
        $ sudo mkdir /mnt/dropbox
        ```
1. Install external dependencies
    - [ffmpeg](https://ffmpeg.org/)
        ```
        $ sudo apt install ffmpeg
        ```
    - [cifs-utils](https://wiki.samba.org/index.php/LinuxCIFS_utils) - If on purely Ubuntu machine use [cifs-utils](https://wiki.samba.org/index.php/LinuxCIFS_utils) to mount Windows samba shares in Ubuntu. (NOTE: This is **NOT** needed for Windows Subsystem Linux)
        ```
        $ sudo apt install cifs-utils
        ```
1. Edit `/etc/fstab`, adding a line for each mount
    ```
    $ sudo nano /etc/fstab
    ```
    - Example for WSL:
        ```
        N:/ /mnt/ffa drvfs defaults 0 0
        L:/ /mnt/satellite drvfs defaults 0 0
        ```
    - Example for Ubuntu Machine
        ```
        //192.168.1.23/dropbox /mnt/dropbox cifs vers=2.0,credentials=/root/cred,iocharset=utf8 0 0

        //192.168.1.32/ffa /mnt/ffa cifs vers=2.0,credentials=/root/other_cred,iocharset=utf8 0 0
        ```
        
1. Create Virtual Environment
    ```
    $ ./environ
    ```
1. Install python dependencies
    ```
    (venv) $ pip install -r requirements.txt
    ```
## Using This Program
This program is meant to be run using the `weekend` script. Simply run the script and it will trigger the program with any flags you enter afterward. 
```
$ ./weekend

$ ./weekend dry

$ ./weekend xds
```
NOTE: If you are running this on an Ubuntu Machine, you may have to run it as root to gain access to the credentials files if they are stored in the root folder (as I have done).

Here is a list of possible flags for the program:
- `sat`, `satellite`, `xds` - run satellite promo processing and file deletion
- `copy` - copy files to remote continuity and dropbox folders
- `clean` - cleans .pkf files leftover from editing files in Adobe Audition
- `reset`, `delete` - deletes all audio files (used to prepare for the next week's files)
- `check`, `stat`, `status` - runs the checking program which shows which files have been downloaded and which have not.
- `mock`, `dry` - dry run
- `process_only`, `process` - run process only, no download
- `thread`, `threading` - using multi-threading to improve performance (use this only on beefier machines that can handle it)
