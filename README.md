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
renaming of files based on air date.
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
    ```bash
    $ sudo apt install ffmpeg
    ```
- [cifs-utils](https://wiki.samba.org/index.php/LinuxCIFS_utils) (not needed on WSL) - Used for mounting Windows network drives from linux
    ```
    $ sudo apt install cifs-utils
    ```
- libraries:
    - python-dotenv
    - ffmpeg-normalize