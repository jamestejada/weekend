import os
import sys
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime


load_dotenv()


def get_date_string() -> str:
    return datetime.now().strftime('%m%d%Y')


def check_flags(flags) -> bool:
    return any([(arg.lower() in flags) for arg in sys.argv[1:]])


def from_cwd(*path_list):
    directory = Path.cwd().joinpath(*path_list)
    directory.mkdir(exist_ok=True, parents=True)
    return directory


class PRX:
    IP = os.getenv('PRX_IP')
    USERNAME = os.getenv('PRX_USERNAME')
    PASSWORD = os.getenv('PRX_PASSWORD')


LOCAL_PATH = from_cwd('files', 'downloads')
FOR_DROPBOX = from_cwd('files', 'for_dropbox')
FOR_FFA = from_cwd('files', 'for_ffa')

_sat_mount = Path(os.getenv('SAT_MOUNT'))
_dropbox_mount = Path(os.getenv('DROPBOX_MOUNT'))
_ffa_mount = Path(os.getenv('FFA_MOUNT'))

SAT_PATH = _sat_mount if _sat_mount.exists() else from_cwd('fake_sat_mount')
DROPBOX_PATH = _dropbox_mount if _dropbox_mount.exists() else from_cwd('fake_dropbox_mount')
FFA_MOUNT = _ffa_mount if _ffa_mount.exists() else from_cwd('fake_ffa_mount')

FFA_PATH = FFA_MOUNT.joinpath('- Corona Continuity Breaks -', 'Promos')
FFA_PATH.mkdir(exist_ok=True, parents=True)

SLACK_WEBHOOK=os.getenv('SLACK_WEBHOOK')

RESET_DIRS = [
    LOCAL_PATH,
    FOR_DROPBOX,
    FOR_FFA
]

# Execution Path Flags
class Execution_Flags:
    PROCESS_ONLY = check_flags(['process_only', 'process'])
    THREAD = check_flags(['thread', 'threading'])
    FORCE_PROCESS = check_flags(['force'])
    DRY_RUN = check_flags(['mock', 'dry'])

    CHECK = check_flags(['check', 'stat', 'status'])
    VERIFY = check_flags(['verify'])
    RESET = check_flags(['reset', 'delete', 'clear'])
    CLEAN = check_flags(['clean'])
    COPY = check_flags(['copy'])
    SAT = check_flags(['sat', 'satellite', 'xds'])
    SLACK = check_flags(['slack', 'bot'])

# LOGGING
LOG_LEVEL = os.getenv('LOG_LEVEL')
LOG_PATH = from_cwd('logs').joinpath(f'weekend-bot-{get_date_string()}.log')
LOG_NAME = 'PRX_WEEKEND_BOT'
