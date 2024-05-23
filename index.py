from dash import html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from app import *
from dash_bootstrap_templates import ThemeSwitchAIO

df = pd.read_csv('database/data.csv')

#Styles
url_theme1 = dbc.themes.VAPOR
url_theme2 = dbc.themes.FLATLY
template_theme1 = 'vapor'
template_theme2 = 'flatly'

# Create a Dash layout
app.layout = dbc.Container([
   dbc.Row([
       dbc.Col([
           ThemeSwitchAIO(aio_id='theme',themes=[url_theme1, url_theme2])
       ])
   ])
])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True, port='8051')