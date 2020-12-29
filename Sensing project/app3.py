import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.graph_objects as go
import random
import plotly
from collections import deque
from datetime import datetime
import csv
import json
import http.client
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

    print(data2)

    with open('weathercsv.csv', 'w') as f: 
        w = csv.DictWriter(f, data2.keys())
        w.writeheader()
    
    

def weathercheck():   
    conn.request("GET", "/current.json?q=London", headers=headers)

    res = conn.getresponse()
    data = res.read()

    data2 = json.loads(data)
    # current_temp = random.randint(0,10)
    current_temp = data2['current']['temp_c']
    current_hum = data2['current']['humidity']
    # current_time = data2['current']['last_updated']
    current_time = datetime.now()
    
    with open('weathercsv.csv', 'a') as f: 
        w = csv.DictWriter(f, data2.keys())
        w.writerow(data2)
        print('data updated')

    return data2, current_temp, current_time, current_hum

data, current_temp, current_time, current_hum = weathercheck()

# print(data)


now = datetime.now()

choice = 0
X = deque(maxlen=40)
Y = deque(maxlen=40)

# X.append(1)
Y.append(1)
available_indicators = ['Temperature (Degrees Celcius)','Humidity','c','d','e','f']

app = dash.Dash(__name__)

app.layout = html.Div([
    
    html.Div([
        dcc.Dropdown(
            id='weatherselector',
            options=[{'label': i, 'value': i} for i in available_indicators],
            value='d'
        ),
    ],
    style={'width': '100%', 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(
            id="live-graph", 
            animate = False,),
        dcc.Interval(
            id='graph-update',
            interval=2000
        ),
    ],style={'display': 'inline-block', 'width': '100%'})
])

@app.callback(
    Output("live-graph", "figure"), 
    [Input('graph-update', 'n_intervals'),
     Input('weatherselector','value')])

def update_graph(timeinterval,weather):

    data, current_temp, current_time, current_hum = weathercheck()
    if weather == 'Temperature (Degrees Celcius)':
        Y.append(current_temp)
    elif weather == 'Humidity':
        Y.append(current_hum)
    else:
        Y.append(0)

    X.append(current_time)

    print(current_temp)

    print(weather)

    data = go.Scatter(
        x = list(X),
        y = list(Y),
        name = 'Scatter',
        mode = 'lines+markers'
        )

    layout = go.Layout(xaxis =dict(title = 'Date&Time' ,range=[min(X), max(X)]),
    yaxis = dict(title = weather, range=[min(Y), max(Y)]),title = 'Time')

    return {
        'data': [data],
        'layout': layout
        }


if __name__ == '__main__':
    app.run_server(debug=False)