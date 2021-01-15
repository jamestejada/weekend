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

PROCESS_ONLY = check_flags(['process_only', 'process'])

