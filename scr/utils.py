

## utilities function

def strlower(series):
    series=series.str.lower()
    series=series.str.strip()
    return series
    
def stripandlower(df,columns=None):
    df.loc[:,columns]=df.loc[:,columns].apply(strlower)
    return df

def write_json_backup_logs(updated_dates):
    if not (BACKUP_LOGS_DIR / 'backup_logs.json').exists():
        ## create file 
        with open(BACKUP_LOGS_DIR / 'backup_logs.json',"w") as fp:
            data={}
            data['logs']=[updated_dates]
            json.dump(data,fp,indent=4)
    else: 
        with open(BACKUP_LOGS_DIR / 'backup_logs.json',) as fp:
            data=json.load(fp)
            temp=data["logs"]
            temp.append(updated_dates)
            
        with open (BACKUP_LOGS_DIR / 'backup_logs.json',"w") as file:
            json.dump(data,file,indent=4)