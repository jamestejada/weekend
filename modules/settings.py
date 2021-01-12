import os
from dotenv import load_dotenv

load_dotenv()

class PRX:
    IP = os.getenv('PRX_IP')
    USERNAME = os.getenv('PRX_USERNAME')
    PASSWORD = os.getenv('PRX_PASSWORD')
