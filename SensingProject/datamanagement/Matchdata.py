import pandas as pd
import json
import csv
import datetime
from datetime import timedelta

def matchweather(golfdata,weatherdata):
    # golfdata = golfdata.head(10000)
    totalrows = len(golfdata)
    weatherlist = {}
    usefulweather = ['utc_last_updated','localtime','lat','lon','temp_c','temp_f','wind_mph','wind_kph','wind_degree',
    'wind_dir','pressure_mb','pressure_in','precip_mm','precip_in','humidity','cloud','feelslike_c',
    'feelslike_f','vis_km','vis_miles','uv','gust_mph','gust_kph']
    for j in usefulweather:
        golfdata[j] = ''
        weatherlist[j] = []
    print(weatherlist)

    # print(weatherdata.keys())
    
    for i in range(totalrows):
        row = golfdata.loc[i]
        time = row['TimeStamp']
        location = row['Range']
        if location == 'Randpark':
            loc = 'Johannesburg'
        else:
            loc = location
        x = weatherdata.loc[weatherdata['name'] == loc] 
        date_time_obj = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
        upper = date_time_obj + timedelta(minutes=7.55)
        lower = date_time_obj - timedelta(minutes=7.55)
        try:
            c = x.loc[x['utc_last_updated'] <= str(upper)]
            d = c.loc[c['utc_last_updated'] >= str(lower)]
            selected = d.iloc[0]
            for item in usefulweather:
                weathervalue = selected[item]
                weatherlist[item].append(weathervalue)
        except:
            print('No Weather Match found')
            for item in usefulweather:
                weathervalue = ''
                weatherlist[item].append(weathervalue)
        print('row {} / {} complete = {:.1f} %'.format(i,totalrows,(i/totalrows*100)))
    for item in weatherlist:
        record = weatherlist[item]
        golfdata[item] = record
    newpath = '/Users/willkerr/Yr 4/SensingIoT/SensingIoT/SensingProject/data/Golf&Weather2.csv'
    golfdata.to_csv(newpath, index=False, encoding='utf-8-sig')
    return golfdata



def additionalparams(data):
    # data = data.head(1000)
    gasconstant = 287.058
    watergasconstant = 461.495
    temp = data['temp_c']
    pressure = data['pressure_mb']
    humidity = data['humidity']/100
    dryair = (pressure*100*(1-0.378*humidity))/(gasconstant*(temp+273.15))
    wetair = (pressure*100*(0.378*humidity))/(watergasconstant*(temp+273.15))
    # dryaironly = (pressure*100)/(gasconstant*(temp+273.15))
    density = dryair+wetair
    density = density.round(2)
    data['air_density'] = density

    curve = data['Curve']
    straightness = -abs(curve)
    data['straightness'] = straightness

    roll = data['Total'] - data['Carry']
    data['Roll'] = roll.round(2)

    newpath = '/Users/willkerr/Yr 4/SensingIoT/SensingIoT/SensingProject/data/Fulldata2.csv'
    data.to_csv(newpath, index=False, encoding='utf-8-sig')
    print(data)

# golf = pd.read_csv("/Users/willkerr/Yr 4/SensingIoT/SensingIoT/SensingProject/Selected_Shots.csv")
# weather = pd.read_csv("/Users/willkerr/Yr 4/SensingIoT/SensingIoT/SensingProject/Selected_Weather.csv")
# x = matchweather(golf,weather)

# data2 = pd.read_csv("/Users/willkerr/Yr 4/SensingIoT/SensingIoT/SensingProject/Golf&Weather2.csv")
# additionalparams(data2)

full = pd.read_csv("/Users/willkerr/Yr 4/SensingIoT/SensingIoT/SensingProject/data/Fulldata.csv")
Ran = full.loc[full['Range'] == 'Randpark' ]
Abd = full.loc[full['Range'] == 'Abu Dhabi' ]
Ldn = full.loc[full['Range'] == 'Greenwich' ]
Ton = full.loc[full['Range'] == 'Tonbridge' ]
Brn = full.loc[full['Range'] == 'Branchburg' ]

Rangelist = [Ran, Abd, Ldn, Ton, Brn]
z = pd.concat(Rangelist)
print(z)