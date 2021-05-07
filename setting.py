from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

DOWNLOAD_DST = os.getenv('DOWNLOADED_DST')
if DOWNLOAD_DST[-1] != '/':
    DOWNLOAD_DST += '/'

HOST_IP = os.getenv('HOST_IP')

DOWNLOAD_PATH_PREFIX = f'http://{HOST_IP}/'
