import numpy as np
import pandas as pd
from math import sin, cos, sqrt, atan2, radians
import datetime
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#Load file
df=pd.read_csv('sample.csv')

#convert latitude and longitude radians for measuring distance
df['radian_lat'] = df.apply(lambda row: radians(row.lat), axis = 1)
df['radian_long'] = df.apply(lambda row: radians(row.long), axis = 1)
df['radian_mlat'] = df.apply(lambda row: radians(row.merch_lat), axis = 1)
df['radian_mlong'] = df.apply(lambda row: radians(row.merch_long), axis = 1)

# Function to Get distance between two points 

# approximate radius of earth in km
def dist(lat1,lon1,lat2,lon2):
    R=6373.0
    dlon=lon2-lon1
    dlat=lat2-lat1

    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))

    return R * c

# Add new column with distance between owner and merchant
df['ownerToMerdist']= dist(df['radian_lat'],df['radian_long'],df['radian_mlat'],df['radian_mlong'])


#add date_time column by converting trans_date_trans_time to date time 
df['date_time']=pd.to_datetime(df['trans_date_trans_time'])
# strip out date and time and add as new column
df['date']=df['date_time'].dt.date
df['time']=df['date_time'].dt.time
# strip out hour and add as new column
df['time_hour']=df['date_time'].dt.hour


# set today to last date of dateset (Dec 31 2020)
today = datetime.datetime(2020, 12, 31)
# convert date of birth to date_time format
df['dob'] =pd.to_datetime(df['dob'], format='%Y/%m/%d')
# set now to last date of dateset (Dec 31 2020)
now = pd.Timestamp('12-31-2020')
# calculate age as of last date of dataset i.e "today"
df['dob'] = df['dob'].where(df['dob'] < now, df['dob'] -  np.timedelta64(100, 'Y'))   
df['age'] = (now - df['dob']).astype('<m8[Y]')    

markdown_text = ''' This dashboard has some visualizations for exploratory data analysis on Fraudulant credit card
transactions '''

### Create app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


app.layout = html.Div(
    [
        html.H1("Exploring Credit Card Fraud"),
        dcc.Markdown(children = markdown_text)
    ]
)
if __name__ == '__main__':
    app.run_server(debug=True, port=8051, host='0.0.0.0')