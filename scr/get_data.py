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

df_storage=get_sheets(
    sheet_filename='Storage_',
    work_sheet_name='Sheet1',
    TITLE_ROW= 1,
    TOKEN_PATH=TOKEN_PATH_SHEETS
)

filt=df_storage['data-Name']=='' ## remove
df_storage=df_storage.loc[~filt]
df=pd.DataFrame()


df=df.assign(
    id=df_storage['data-meta-instanceID'],
    email=df_storage['data-e-mail'].replace({'Unspecified':pd.NA}),
    phone=df_storage['data-phone_1_-_Value'].apply(lambda x:'977'+ x if x!='null' else pd.NA),
    name=df_storage['data-Name'],
    ct=df_storage['data-address_1_-_city'].apply(str.lower).replace({'unspecified':pd.NA}).values,
    country='NP',
    dob=df_storage['data-Year_of_Birth'],
    today=df_storage['data-today'],
    photo_id=[get_pic_id(photo) for photo in df_storage['data-photo'].values],
    fn=lambda d: d['name'].apply(get_fn),
    ln=lambda d: d['name'].apply(get_ln),
    age=lambda d: d['dob'].apply(get_age),
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
df=df.loc[lambda df: df['name'] != df['name'].isna(),]

data_storage_path=INPUT_DATA_PATH
def export_data(df):
    df.to_csv(data_storage_path,index=None)
export_data(df)