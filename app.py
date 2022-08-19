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


#Distribution by time for fraudulant vs. non-fradualant transactions
fig_time = px.histogram(df, x="time_hour",color="is_fraud",histnorm='probability density',
                        marginal='box',opacity=0.5,
                       labels={"time_hour": "Time of Transaction"})
fig_time.update_layout(barmode='overlay')
#fig_time.update_xaxes(title_text='Time of Transaction')
fig_time.show()

#Distribution by age for fraudulant vs. non-fradualant transactions
fig_age = px.histogram(df, x="age",color="is_fraud",histnorm='probability density',
                       marginal="box",opacity=0.5,nbins=15,labels={
                     "age": "Age of card holder"})
fig_age.update_layout(barmode='overlay')
fig_age.show()

#Distribution by distance for fraudulant vs. non-fradualant transactions
fig_dist = px.histogram(df, x="ownerToMerdist",color="is_fraud",histnorm='probability density',marginal='box',
                        opacity=0.5,nbins=15,
                       labels={"ownerToMerdist": "Distance between transaction and card holder"})
fig_dist.update_layout(barmode='overlay')
fig_dist.show()


#Distribution by amount for fraudulant vs. non-fradualant transactions
fig_amt = px.histogram(df.query("amt<3000"), x="amt",color="is_fraud",histnorm='probability density',marginal="box",
                       opacity=0.5,nbins=100,labels={"amt": "$ Amount of Transaction"}
                      )
fig_amt.update_layout(barmode='overlay')
#fig_amt.update_xaxes(title_text='$ Amount of Transaction')
fig_amt.show()



markdown_text = ''' This dashboard has some visualizations for exploratory data analysis on Fraudulant credit card
transactions '''

### Create app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


app.layout = html.Div(
    [
        html.H1("Exploring Credit Card Fraud"),
        dcc.Markdown(children = markdown_text),
        html.Div([
            
            html.H2("Distribution by Transaction Time"),
            
            dcc.Graph(figure=fig_time)
            
        ], style = {'width':'48%', 'float':'left'}),
        
        html.Div([
            
            html.H2("Distribution by Age Group"),
            
            dcc.Graph(figure=fig_age)
            
        ], style = {'width':'55%', 'float':'right'}),
        html.Div([
            
            html.H3("Distribution by Distance of card owner address to Transaction (km)"),
            
            dcc.Graph(figure=fig_dist)
            
        ], style = {'width':'43%', 'float':'left'}),
        html.Div([
            
            html.H3("Distribution by Transaction Amount"),
            
            dcc.Graph(figure=fig_amt)
            
        ], style = {'width':'48%', 'float':'right'})
    ]
)
if __name__ == '__main__':
    app.run_server(debug=True, port=8051, host='0.0.0.0')