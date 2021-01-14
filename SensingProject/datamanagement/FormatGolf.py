import pandas as pd
import json
import csv
import datetime
from datetime import timedelta

def launch_vel_calc(data,row):
    lv2 = data['LaunchVelocity'][row]
    index_x = lv2.find('x')
    index_y = lv2.find('y')
    index_z = lv2.find('z')
    lv3 = (lv2[:index_x] + "'" + lv2[index_x:index_x+1] + "'" + lv2[index_x+1:index_y] + "'" + lv2[index_y:index_y+1]+ "'" + lv2[index_y+1:index_z]+ "'" + lv2[index_z:index_z+1]+ "'" + lv2[index_z+1:])
    lv4 = lv3.replace("'", "\"")
    lvjs = json.loads(lv4)
    x = lvjs['x']
    y = lvjs['y']
    z = lvjs['z']
    rv = (x*x + y*y + z*z)**0.5
    resultantvel= '{:.5f}'.format(rv)
    data['Launch_Velocity'][row] = resultantvel
    
def curvecalc(data,row):
    curve = data['Curve'][row]
    if 'R' in curve:
        c = curve.replace("R", "")
        newcurve = float('+{}'.format(c))
    elif 'L' in curve:
        c = curve.replace("L", "")
        newcurve = float('-{}'.format(c))
    else:
        newcurve = float(curve)
    data['Curve'][row] = newcurve

def reformat(data):
    rowcount = 0
    totalrows = len(data)
    for row in range(totalrows):
        launch_vel_calc(data,row)
        curvecalc(data,row)
        rowcount+=1
        print('Rowcount is {} / {}'.format(rowcount,totalrows))
    return data
  
def work(df):
    newpath = '/Users/willkerr/Yr 4/SensingIoT/SensingIoT/SensingProject/data/GolfdataReformatted.csv'
    data = reformat(df)
    Not = (data[data['Range'] == 'Nottingham'].index)
    data = data.drop(data.index[Not])
    data = data.drop(['LaunchVelocity'], axis=1)
    print(data['Launch_Velocity'])
    print(data.head())
    data.to_csv(newpath, index=False, encoding='utf-8-sig')

def select_shots():
    data = pd.read_csv("/Users/willkerr/Yr 4/SensingIoT/SensingIoT/SensingProject/data/GolfdataReformatted.csv")
    start_time = '2020-12-29 17:30:00'
    end_time = '2021-01-04 06:16:00'
    baddates = []
    totalrows = len(data)
    print(totalrows)
    for row in range(totalrows):
        time = data['TimeStamp'][row]
        if time <= start_time or time >= end_time:
            # print('{} not within interval'.format(time))
            baddates.append(data.index[row])
            # print('{}within interval'.format(time))
    print(baddates)
    print(len(baddates))
    newdata = data.drop(data.index[baddates])
    newpath = '/Users/willkerr/Yr 4/SensingIoT/SensingIoT/SensingProject/data/Selected_Shots.csv'
    newdata.to_csv(newpath, index=False, encoding='utf-8-sig')

df = pd.read_csv("/Users/willkerr/Yr 4/SensingIoT/SensingIoT/SensingProject/data/Golfdata.csv")
# work(df)
