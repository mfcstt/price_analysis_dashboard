from dash import html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from app import *
from dash_bootstrap_templates import ThemeSwitchAIO

# Read the data
df = pd.read_csv('database/data.csv')
state_options = [{'label': x, 'value': x} for x in df['ESTADO'].unique()]

#Styles
url_theme1 = dbc.themes.DARKLY
url_theme2 = dbc.themes.MINTY
template_theme1 = 'darkly'
template_theme2 = 'minty'

# Create a Dash layout
app.layout = dbc.Container([
   dbc.Row([
       dbc.Col([
           ThemeSwitchAIO(aio_id='theme',themes=[url_theme1, url_theme2]),
           html.H3('Preço x Estado'),
           dcc.Dropdown(
               id='estados',
               value=[state['label'] for state in state_options[:3]],
               multi=True,
               options=state_options,
           ),
           dcc.Graph(id='line_graph')
       ])
   ]),
   dbc.Row([
       dbc.Col([
           dcc.Dropdown(
               id='estado01',
               value=state_options[0]['label'],
               options=state_options
           )
       ], sm=12, md=6),
       dbc.Col([
           dcc.Dropdown(
               id='estado02',
                value=state_options[1]['label'],
                options=state_options
           )
       ], sm=12, md=6),
       dbc.Col([
           dcc.Graph(id='indicator_graph')
       ], sm=6),
       dbc.Col([
           dcc.Graph(id='indicator_graph2')
       ], sm=6)
   ])
])

# Callback
@app.callback(
    Output('line_graph', 'figure'),
    Input('estados', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
)
def line(estados, toggle_theme):
    template = template_theme1 if toggle_theme else template_theme2
    
    
    df_data = df.copy(deep=True)
    mask = df_data['ESTADO'].isin(estados)
    fig = px.line(df_data[mask], x='DATA', y='VALOR REVENDA (R$/L)',
                     color='ESTADO', template=template)
    return fig

@app.callback(
    Output('indicator_graph', 'figure'),
    Output('indicator_graph2', 'figure'),
    Input('estado01', 'value'),
    Input('estado02', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
)
def indicators(estado01, estado02, toggle_theme):
    template = template_theme1 if toggle_theme else template_theme2
    
    df_data = df.copy(deep=True)
    data_estado01 = df_data[df_data.ESTADO.isin([estado01])]
    data_estado02 = df_data[df_data.ESTADO.isin([estado02])]
    
    initial_date = str(df_data['ANO'].min() -1)
    final_date = df_data['ANO'].max()
    
    
    iterable = [(estado01, data_estado01), (estado02, data_estado02)]
    indicators = []
    
    for estado, data in iterable:
        fig = go.Figure()
        fig.add_trace(go.Indicator(
            mode = "number+delta",
            title = {"text": f"<span>{estado}</span><br><span style='font-size:0.7em'>{initial_date} - {final_date}</span>"},
            value = data.at[data.index[-1],'VALOR REVENDA (R$/L)'],
            number = {'prefix': "R$", 'valueformat': '.2f'},
            delta = {'relative': True, 'valueformat': '.1%', 'reference': data.at[data.index[0],'VALOR REVENDA (R$/L)']}
        ))
        fig.update_layout(template=template)
        indicators.append(fig)
    
    return indicators

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True, port='8051')