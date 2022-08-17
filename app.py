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