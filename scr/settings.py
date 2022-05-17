from pathlib import Path

## all the path information##

BASE_DIR=Path(__file__).parent.parent
DESKTOP_DIR= Path.home()/ "Desktop"

##credential path
CREDS_DIR=BASE_DIR / 'creds'
CLIENT_SECRET_FILE=CREDS_DIR / 'client_secret.json'
PIC_DIR_PATH=DESKTOP_DIR / "HRIS" #where image will be saved
TOKEN_DIR=BASE_DIR / "creds"
TOKEN_PATH_SHEETS=TOKEN_DIR / "token_sheets.json"
TOKEN_PATH_DRIVE=TOKEN_DIR / "token_drive_v3.pickle"
INPUT_DIR=BASE_DIR / "input"

if not CREDS_DIR.exists():
    CREDS_DIR.mkdir(parents=True,exist_ok=True)

if not PIC_DIR_PATH.exists():
    PIC_DIR_PATH.mkdir(parents=True,exist_ok=True)

if not INPUT_DIR.exists():
    INPUT_DIR.mkdir(parents=True,exist_ok=True)

INPUT_DATA_PATH= INPUT_DIR / 'storage_data.csv'

## drive api information

API_NAME='drive'
API_VERSION= 'v3'
SCOPES=['https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.metadata']