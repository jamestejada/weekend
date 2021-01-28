import os
import sys
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


def check_flags(flags) -> bool:
    return any([(arg in flags) for arg in sys.argv[1:]])


def from_cwd(*path_list):
    directory = Path.cwd().joinpath(*path_list)
    directory.mkdir(exist_ok=True, parents=True)
    return directory


class PRX:
    IP = os.getenv('PRX_IP')
    USERNAME = os.getenv('PRX_USERNAME')
    PASSWORD = os.getenv('PRX_PASSWORD')


LOCAL_PATH = from_cwd('downloads')
FOR_DROPBOX = from_cwd('for_dropbox')
FOR_FFA = from_cwd('for_ffa')

RESET_DIRS = [LOCAL_PATH, FOR_DROPBOX, FOR_FFA]


PROCESS_ONLY = check_flags(['process_only', 'process'])
RESET = check_flags(['reset', 'delete'])
THREAD = check_flags(['thread', 'threading'])
FORCE_PROCESS = check_flags(['force'])
DRY_RUN = check_flags(['mock', 'dry'])