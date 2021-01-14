import pandas as pd
import json
import csv
import datetime
from datetime import timedelta

Rangenames = ['Greenwich,London','Johannesburg,South-Africa','Tonbridge','Branchburg','Abu-Dhabi']
New_csvs = ['LDN','SA','TNB','BNB','ABD']
def utctime(data,row):
    loc = data['location'][row]
    loc1 = loc.replace("'", "\"")
    locjs = json.loads(loc1)

    utc_local = locjs['localtime_epoch']
    utc_local_format = datetime.datetime.utcfromtimestamp(utc_local).strftime('%Y-%m-%d %H:%M:%S')
    utc_local_dict = {'utc_local_time':utc_local_format}


    cur = data['current'][row]
    cur1 = cur.replace("'", "\"")
    curjs = json.loads(cur1)

    print(cur)
    print(cur1)
    print(curjs)
    

    utc_updated = curjs['last_updated_epoch']
    utc_updated_format = datetime.datetime.utcfromtimestamp(utc_updated).strftime('%Y-%m-%d %H:%M:%S')
    utc_updated_dict = {'utc_last_updated':utc_updated_format}


    curjs.pop('is_day')
    curjs.pop('condition')
    # print(curjs)
    combined = {**locjs,**utc_local_dict,**utc_updated_dict,**curjs}
    # print(combined)
    return combined
def update_header(data,newpath):
    rowcount = 0
    combined = utctime(data,rowcount)
    with open(newpath, 'w') as f: 
                w = csv.DictWriter(f, combined.keys())
                w.writeheader()
                print('Header updated')
def reformat_csv(data,newpath):
    rowcount = 0
    totalrows = len(data)
    for row in range(totalrows):
        combined = utctime(data,row)
        with open(newpath, 'a') as f: 
            w = csv.DictWriter(f, combined.keys())
            w.writerow(combined)
            rowcount += 1
            print('row {} / {} updated'.format(rowcount,totalrows))
def work():
    count = 0
    for i in Rangenames:
        path = '/Users/willkerr/Yr 4/SensingIoT/SensingIoT/SensingProject/data/{}'.format(i+'.csv')
        df = pd.read_csv(path)
        j = New_csvs[count]
        newpath = '/Users/willkerr/Yr 4/SensingIoT/SensingIoT/SensingProject/data/{}'.format(j+'.csv')
        update_header(df,newpath)
        reformat_csv(df,newpath)
        count+=1
work()

def testrange():
    i = 'TestRange'
    path = '/Users/willkerr/Yr 4/SensingIoT/SensingIoT/SensingProject/data/{}'.format(i+'.csv')
    df = pd.read_csv("/Users/willkerr/Yr 4/SensingIoT/SensingIoT/SensingProject/data/Abu-Dhabi.csv")
    update_header(df,path)
    reformat_csv(df,path)

def combine_csvs(New_csvs):
    csv_list =[]
    for i in New_csvs:
        path = '/Users/willkerr/Yr 4/SensingIoT/SensingIoT/SensingProject/data/{}'.format(i+'.csv')
        df = pd.read_csv(path)
        csv_list.append(df)
    testcombined_csv = pd.concat(csv_list)

    newpath = '/Users/willkerr/Yr 4/SensingIoT/SensingIoT/SensingProject/data/Combined_Weather.csv'
    testcombined_csv.to_csv(newpath, index=False, encoding='utf-8-sig')

def selectdates():
    # rowcount = 0
    data = pd.read_csv("/Users/willkerr/Yr 4/SensingIoT/SensingIoT/SensingProject/data/Combined_Weather.csv")
    start_time = '2020-12-29 17:30:00'
    end_time = '2021-01-04 06:16:00'
    baddates = []
    totalrows = len(data)
    print(totalrows)
    for row in range(totalrows):
        time = data['utc_last_updated'][row]
        if time <= start_time or time >= end_time:
            # print('{} not within interval'.format(time))
            baddates.append(data.index[row])
            # print('{}within interval'.format(time))
    print(baddates)
    print(len(baddates))
    newdata = data.drop(data.index[baddates])
    
    newpath = '/Users/willkerr/Yr 4/SensingIoT/SensingIoT/SensingProject/data/Selected_Weather.csv'
    newdata.to_csv(newpath, index=False, encoding='utf-8-sig')

selectdates()




# combine_csvs(New_csvs)




