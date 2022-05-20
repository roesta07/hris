import numpy as np
import pandas as pd
from urllib.parse import urlencode,urlparse,parse_qsl
from .Google import Create_Service
from .settings import *
from googleapiclient.http import MediaIoBaseDownload
import datetime as dt
from .sheet_utils import get_sheets
from PIL import Image
import io


# filter useless

service=Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,TOKEN_PATH_DRIVE,SCOPES)

def get_pic_id(x):
    try:
        id_name=x.split("=")[1]
        return id_name
    except (IndexError, AttributeError):
        return pd.NA

def get_fn(x):
    fn=x.split(' ')[0]
    return fn
def get_ln(x):
    ln=x.split(' ')[-1]
    return ln


def get_age(dob):
    try:
        birth_date=dt.datetime.strptime(dob,'%d/%m/%y')
        today=dt.datetime.today()
        age_year=((today-birth_date).days)/365
        return age_year
    except ValueError:
        return np.NaN


## getting data from sheets
df_storage=get_sheets(
    sheet_filename='Storage_',
    work_sheet_name='Sheet1',
    TITLE_ROW= 1,
    TOKEN_PATH=TOKEN_PATH_SHEETS
)

filt=df_storage['data-Name']=='' ## remove
df_storage=df_storage.loc[~filt]
df=pd.DataFrame()


df_storage=get_sheets(
    sheet_filename='Storage_',
    work_sheet_name='Sheet1',
    TITLE_ROW= 1,
    TOKEN_PATH=TOKEN_PATH_SHEETS
)

df=df.assign(
    name=df_storage['data-Name'],
    gender=df_storage['data-Gender'],
    email=df_storage['data-e-mail'].replace({'Unspecified':pd.NA}),
    phone=df_storage['data-phone_1_-_Value'].apply(lambda x:'977'+ x if x!='null' else pd.NA),
    ct=df_storage['data-address_1_-_city'].apply(str.lower).replace({'unspecified':pd.NA}).values,
    country='NP',
    rod=pd.to_datetime(df_storage['data-today'],format="%d/%m/%y",errors='coerce'),
    dob=df_storage['data-Year_of_Birth'],
    today=df_storage['data-today'],
    photo_id=[get_pic_id(photo) for photo in df_storage['data-photo'].values],
    fn=lambda d: d['name'].apply(get_fn),
    ln=lambda d: d['name'].apply(get_ln),
    age=lambda d: d['dob'].apply(get_age),
    id=df_storage['data-meta-instanceID'],
    lisc=df_storage['data-Driving_License'].replace({
        'Unspecified':'idk', 'no':'False', 'category_a__motorcycle_scooter':'A',
        'category_a__motorcycle_scooter':'A', 'category_b__car_jeep_delivery':"B",
        'category_k__scooter__moped':"K", '':'idk', 'yes':'True',
        'category_a__motorcycle_scooter':"A",
        'category_a__motorcycle_scooter, no':"A",
        'category_b__car_jeep_delivery':"B",
        'category_b__car_jeep_delivery':"B", "category_a__motorcycle_scooter":"A",
        'no, category_a__motorcycle_scooter':"A",
        'category_b__car_jeep_delivery, category_a__motorcycle_scooter':'AB',
        'category_a__motorcycle_scooter, category_b__car_jeep_delivery':'AB',
})
)

empty_id_filter=df['photo_id'].isna()
df_filtered=df.loc[~empty_id_filter]

DONE_FILE_CSV_PATH=BASE_DIR / "scr" / "done.csv"

if not DONE_FILE_CSV_PATH.exists():
    df_done=pd.DataFrame(columns=df.columns)
    df_done.to_csv(DONE_FILE_CSV_PATH,index=None)

existing_pics=pd.read_csv("scr/done.csv").phone.values
already_downloaded_filt= np.array([True if pic in existing_pics else False for pic in df_filtered['phone']])
print(~already_downloaded_filt)
df_filtered=df_filtered.loc[~already_downloaded_filt]

def assign_filename(df_filtered):
    lst=[]
    for name,phone,lis in zip(
                    df_filtered['name'],
                    df_filtered['phone'],
                    df_filtered['lisc']):
     
        lst.append(f'{name}_{phone}_{lis}.jpg')
    return np.array(lst)

file_ids=df_filtered['photo_id'].values
file_names=assign_filename(df_filtered)

def download_media(service,file_ids,file_names,pic_store_path):
    for file_id,file_name in zip(file_ids,file_names,):
        request = service.files().get_media(fileId=file_id,)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print ("Download %d%%." % int(status.progress() * 100))
        pic=Image.open(fh)
        pic.save(pic_store_path / f'{file_name}')
    df_filtered.to_csv('scr/done.csv',mode="a")
    print("Updated; thank you for your patience")


download_media(
    service=service,
    file_ids=file_ids,
    file_names=file_names,
    pic_store_path=PIC_DIR_PATH
    )