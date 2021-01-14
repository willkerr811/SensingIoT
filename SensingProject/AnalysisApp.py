# Import required python libraries
import csv
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import datetime
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import seaborn as sns
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
from pathlib import Path


# Reading data files from directory
# Update directory path as suitable.

path1 = '/Users/willkerr/Yr 4/SensingIoT/SensingIoT/SensingProject/data/Fulldata2.csv'
df = pd.read_csv(path1)
path2 = '/Users/willkerr/Yr 4/SensingIoT/SensingIoT/SensingProject/data/CorrelationMatrix.csv'
matrix = pd.read_csv(path2)
variables = list(df)
colorscales = px.colors.named_colorscales()

# Function used to plot correlation matrix using MatPlotLib

def plotcorrmatrix(data):
    corrmatrix= data.corr()
    newpath = '/Users/willkerr/Yr 4/SensingIoT/SensingIoT/SensingProject/CorrelationMatrix.csv'
    corrmatrix.to_csv(newpath, index=False, encoding='utf-8-sig')
    f = plt.figure(figsize=(6, 6))
    plt.matshow(corrmatrix, fignum=f.number)
    plt.xticks(range(data.select_dtypes(['number']).shape[1]), data.select_dtypes(['number']).columns, fontsize=5, rotation=70)
    plt.yticks(range(data.select_dtypes(['number']).shape[1]), data.select_dtypes(['number']).columns, fontsize=5)
    cb = plt.colorbar()
    cb.ax.tick_params(labelsize=5)
    plt.title('Correlation Matrix', fontsize=10)
    plt.show()
# plotcorrmatrix(df)

# Function to quickly plot a graph using Plotly
def plotgraph(data,xdata,ydata):
    fig2 = px.scatter(data,x=xdata,y=ydata,color='Range')
    fig2.show()

# Function to calcualte total shot distances at different ranges
def totals(df):
    Ranges = ['Greenwich','Tonbridge','Randpark','Abu Dhabi','Branchburg']
    totals = []
    for i in Ranges:
        x = df.loc[df['Range'] == i]
        tot = x['Total']
        sumtot = tot.sum()/1000
        totals.append(sumtot)
        print("{}'s total distantce = {:.2f}km".format(i,sumtot))
    
    allrangesdist = sum(totals)
    equator = 40075
    equartorpercentage = allrangesdist/equator * 100
    formatted = '{:.2f}%'.format(equartorpercentage)
    print("All Ranges's total distantce = {:.2f}km".format(allrangesdist))
    print("That's {} around the equator!".format(formatted))

    return totals, allrangesdist

# Start of app code
app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Img(src='/assets/inrangelogo.png',style={'width':'10%'}),
        html.H1(children='⛳  Weather Analysis App  🌧️')
    ],
    style={'backgroundColor': 'rgb(4, 26, 39)','padding': '20px 5px 20px','textAlign': 'center'}),

    html.Div([
        html.H4(children='A look at how the weather at our ranges has impacted golf this week (29 December - 4 January).')
    ],
    style={'backgroundColor': 'rgb(242, 10, 147)','padding': '5px 0px 5px','textAlign': 'center'}),

    html.Div([
        html.Div([
            html.H3(children='What do you want to plot on the x axis?')
        ]),
        html.Div([
            dcc.Dropdown(
                id='xaxis',
                options=[{'label': i, 'value': i} for i in variables],
                value='TimeStamp' 
            ),
        ],
        style={'width': '100%', 'display': 'inline-block'}),
        html.Div(
            html.H3(children='What do you want to plot on the y axis?')
        ),
        html.Div([
            dcc.Dropdown(
                id='yaxis',
                options=[{'label': i, 'value': i} for i in variables],
                value='Carry' 
            ),
            html.Div(
            html.H3(children='What type of chart do you want to view?')
            ),
            dcc.RadioItems(
                id='graphtype',
                options=[{'label': i, 'value': i} for i in ['Scatter', 'Box','Line']],
                value='Scatter',
                labelStyle={'display': 'inline-block'}
            ),

            html.Div(
            html.H3(children='Select Ranges')
            ),
            dcc.Checklist(
                id = 'rangechecklist',
                options=[
                    {'label': 'Abu Dhabi, UAE', 'value': 'Abu Dhabi'},
                    {'label': 'Randpark, SA', 'value': 'Randpark'},
                    {'label': 'Greenwich, UK', 'value': 'Greenwich'},
                    {'label': 'Branchburg, USA', 'value': 'Branchburg'},
                    {'label': 'Tonbridge, UK', 'value': 'Tonbridge'}
                    ],
                value=['Abu Dhabi', 'Randpark','Greenwich','Branchburg','Tonbridge'],
                labelStyle={'display': 'inline-block','padding': '0px 5px 0px'}
            ),

            html.Div(
            html.H3(children='Filter by shot Carry distance (m)')
            ),
            dcc.RangeSlider(
                id='Shotsslider',
                min=0,
                max=350,
                step=0.5,
                value=[0, 350],
                allowCross=False,
                marks={
                    0: '0 m',
                    50: '50 m',
                    100: '100 m',
                    150: '150 m',
                    200: '200 m',
                    250: '250 m',
                    300: '300 m',
                    350: '350 m',
                },
            ),
            html.Div(
                html.H5(children='Minimum Carry: 0 m, Maximum Carry 350 m:', 
                        id='output-container-range-slider',
                        style={'textAlign': 'center'})
                ),
                
        ],
        style={'width': '100%', 'display': 'inline-block'}),
    ],
    style={'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '5px 5px 10px'}),

    html.Div([
        dcc.Graph(
            id="graph",
            style={'display': 'inline-block','width': '100%','height': '85vh'}
        )
    ], 
    style={'display': 'inline-block','width': '100%'}),

    html.Div([
        html.H1(children='📈  Correlation Matrix  📉')
    ],
    style={'backgroundColor': 'rgb(4, 26, 39)','padding': '10px 5px 10px','textAlign': 'center'}),

    html.Div([
        html.H4(children='Hover over the heatmap to see exact linear correlations between variables'),
    ],
    style={'backgroundColor': 'rgb(242, 10, 147)','padding': '5px 0px 5px','textAlign': 'center'}),

    html.Div([

        html.Div([
            html.H3(children='Filter correlation matrix? Set the minimum correlation value e.g. ±0.5'),
            dcc.RadioItems(
                id='matrixtype',
                options=[{'label': i, 'value': i} for i in ['Normal', 'Filtered']],
                value='Normal',
                labelStyle={'display': 'inline-block'},
                style={'padding': '5px 0px 10px'}
            ),
            dcc.Slider(
                id='Corrslider',
                min=0,
                max=0.99,
                step=0.01,
                value=0.0,
                marks={
                    0.0: '±0.0',
                    0.1: '±0.1',
                    0.2: '±0.2',
                    0.3: '±0.3',
                    0.4: '±0.4',
                    0.5: '±0.5',
                    0.6: '±0.6',
                    0.7: '±0.7',
                    0.8: '±0.8',
                    0.9: '±0.9',
                    1.0: '±1.0',
                },
            ),
            html.Div(
                html.H5(children='Minimum Corellation Value: 0.0', 
                        id='output-container-matrix-slider',
                        style={'textAlign': 'center'})
            ),

        ]),

    ],
    style={'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '5px 5px 10px'}),

    html.Div([
        dcc.Graph(
            id="matrixgraph",
            style={'display': 'inline-block','width': '60%','height': '90vh','textAlign': 'center'}
        )
    ], 
    style={'display': 'inline-block','width': '100%','textAlign': 'center'}),

    # Future section for automated insights
    # html.Div([
    #     html.H1(children='Insights  💡')
    # ],
    # style={'backgroundColor': 'rgb(4, 26, 39)','padding': '10px 5px 10px','textAlign': 'center'}),

    # html.Div([
    #     html.H4(children="An overview of the week's results"),
    # ],
    # style={'backgroundColor': 'rgb(242, 10, 147)','padding': '5px 0px 5px','textAlign': 'center'}),

    # html.Div([

    #     html.H5(children='Section in development', style={'textAlign': 'center'}),
    #     html.H5(children='Hello',id='output-container-stats',style={'textAlign': 'center'})
        
    # ]),
])
@app.callback(
    Output("graph", "figure"), 
    [Input('xaxis', 'value'),
    Input('yaxis','value'),
    Input('graphtype','value'),
    Input('Shotsslider','value'),
    Input('rangechecklist','value')])
def update_graph(weatheraxis,golfaxis,graphtype,shotrange,ranges):
    selected = []
    for i in ranges:
        Ran = df.loc[df['Range'] == i]
        selected.append(Ran)
    newdf = pd.concat(selected)
    lowerbound = str(shotrange[0])
    upperbound = str(shotrange[1])
    data = newdf.query('Carry > {}'.format(lowerbound))
    data = data.query('Carry < {}'.format(upperbound))
    xdata = weatheraxis
    ydata = golfaxis
    if graphtype == 'Scatter':  
        fig2 = px.scatter(data,x=xdata,y=ydata,color='Range')
    elif graphtype == 'Box': 
        fig2 = px.box(data,x=xdata,y=ydata,color='Range')
    elif graphtype == 'Line': 
        fig2 = px.line(data,x=xdata,y=ydata,color='Range')
    return fig2

@app.callback(
    Output("matrixgraph", "figure"),
    [Input('xaxis', 'value'),
    Input('Shotsslider','value'),
    Input('matrixtype','value'),
    Input('Corrslider', 'value'),
    Input('rangechecklist','value')])
def update_matrix(matrix,shotrange,matrixtype,corrvalue,ranges):
    selected = []
    for i in ranges:
        Ran = df.loc[df['Range'] == i]
        selected.append(Ran)
    newdf = pd.concat(selected)
    lowerbound = str(shotrange[0])
    upperbound = str(shotrange[1])
    data = newdf.query('Carry > {}'.format(lowerbound))
    data = data.query('Carry < {}'.format(upperbound))
    corrmatrix= data.corr()
    x = corrvalue
    filteredmatrix = corrmatrix[((corrmatrix >= x) | (corrmatrix <= -x)) & (corrmatrix !=1.000)]
    if matrixtype == 'Normal':
        fig = px.imshow(corrmatrix, color_continuous_scale='Tropic_r')
    elif matrixtype == 'Filtered':
        fig = px.imshow(filteredmatrix, color_continuous_scale='Tropic_r')
    return fig

@app.callback(
    Output("output-container-range-slider", "children"),
    [Input('Shotsslider', 'value')])
def update_slideroutput(value):
    lower = str(value[0]) +' m'
    upper = str(value[1]) +' m'
    newtext = ('Minimum Carry: {}, Maximum Carry: {}'.format(lower,upper))
    return newtext

@app.callback(
    Output("output-container-matrix-slider", "children"),
    [Input('Corrslider', 'value')])
def update_slideroutput2(value):
    newtext = ('Minimum Corellation Value: {}'.format(value))
    return newtext

#     Section for future development
# @app.callback(
#     Output("output-container-stats", "children"),
#     [Input('Corrslider', 'value')])
# def update_stats(shotrange):
#     newtext = 'Section in development'
#     return newtext


if __name__ == '__main__':
    app.run_server(debug=False)


