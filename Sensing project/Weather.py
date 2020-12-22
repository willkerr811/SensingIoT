import http.client
import json
import csv
import time

conn = http.client.HTTPSConnection("weatherapi-com.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "9a65ca1584msh65e042d39a9f35cp1b90bajsn21393d526e0a",
    'x-rapidapi-host': "weatherapi-com.p.rapidapi.com"
    }

def createcsv():

    conn.request("GET", "/current.json?q=Greenwich,London", headers=headers)

    res = conn.getresponse()
    data = res.read()

    data2 = json.loads(data)

    with open('weathercsv.csv', 'w') as f: 
        w = csv.DictWriter(f, data2.keys())
        w.writeheader()
    

def weathercheck():
    
    conn.request("GET", "/current.json?q=Johannesburg", headers=headers)

    res = conn.getresponse()
    data = res.read()

    data2 = json.loads(data)

    print(data2)
    

    with open('weathercsv.csv', 'a') as f: 
        w = csv.DictWriter(f, data2.keys())
        w.writerow(data2)
        print('data updated')


        
weathercheck()