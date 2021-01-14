import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class PRX:
    IP = os.getenv('PRX_IP')
    USERNAME = os.getenv('PRX_USERNAME')
    PASSWORD = os.getenv('PRX_PASSWORD')

LOCAL_PATH = Path().joinpath('downloads')
LOCAL_PATH.mkdir(parents=True, exist_ok=True)

