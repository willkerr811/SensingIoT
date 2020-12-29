import http.client
import json
import csv
import time

conn = http.client.HTTPSConnection("weatherapi-com.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "9a65ca1584msh65e042d39a9f35cp1b90bajsn21393d526e0a",
    'x-rapidapi-host': "weatherapi-com.p.rapidapi.com"
    }

Rangenames = ['Greenwich,London','Johannesburg,South-Africa','Tonbridge','Branchburg','Abu-Dhabi']

def createcsv(Rangenames):

    conn.request("GET", "/current.json?q=Greenwich,London", headers=headers)

    res = conn.getresponse()
    data = res.read()

    data2 = json.loads(data)

    for i in Rangenames:
        with open(i+'.csv', 'w') as f: 
            w = csv.DictWriter(f, data2.keys())
            w.writeheader()
    

def weathercheck(ranges):

    for i in ranges:    
        conn.request("GET", "/current.json?q={}".format(i), headers=headers)
        res = conn.getresponse()
        data = res.read()

        data2 = json.loads(data)

        print(data2)
        
        # with open('weathercsv.csv', 'a') as f: 
        #     w = csv.DictWriter(f, data2.keys())
        #     w.writerow(data2)
        #     print('data updated')

        with open(i+'.csv', 'a') as f: 
            w = csv.DictWriter(f, data2.keys())
            w.writerow(data2)
            print('data updated')

#createcsv(Rangenames)
weathercheck(Rangenames)