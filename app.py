import plotly_express as px
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output


import pandas as pd

#url = 'https://raw.githubusercontent.com/AntiDeprime/whitecounter/master/data.csv'
df = pd.read_csv('./data.csv', parse_dates=['date'], usecols=['date', 'name', 'count', 'coord'])
df.dropna(inplace=True)

df[['lat', 'lon']] = df['coord'].str.split(', ' ,expand=True).astype('float')
df.sort_values(by=['date'], ascending=False)
df['date_str'] = df['date'].dt.strftime('%Y-%m-%d')
df1 = df.set_index('date')
df['Q'] = df.date.dt.quarter
df['M'] = df.date.dt.month
df['D'] = df.date.dt.dayofyear
df['Y'] = df.date.dt.year



token = 'pk.eyJ1IjoiYW50aWRlcHJpbWUiLCJhIjoiY2syYzBwdXVxMDl3eDNicW9pbTE2dzJ5MCJ9.3_OL4GUnwOryXefKh73ZVw'
px.set_mapbox_access_token(token)


fig = px.scatter_mapbox(df, 
                        lat="lat", 
                        lon="lon",  
                        color="count", 
                        size="count",
                        color_continuous_scale=px.colors.cyclical.IceFire, 
                        size_max=15, 
                        zoom=10, 
                        #animation_frame='date_str',  
                        )

df_q_sum = df1.resample('Q').sum().reset_index()
df_q_count = df1.resample('Q').count().reset_index()

hist = px.line(df_q_sum, 
                x="date", 
                y='count', 
                line_shape="spline",)

hist.layout.height = 200



app = dash.Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)

app.layout = html.Div(
    [


        html.H1("White Counter Protests Data"),
        dcc.Graph(id="graph", style={"width": "100%", "display": "inline-block"},
        
        #figure=fig 
        ),

        dcc.Graph(id="hist", style={"width": "100%", "display": "inline-block"},
        
        figure=hist 
        ),




        html.Button('Submit', id='button'),
    ]
)

@app.callback (
    Output('graph', 'figure'),
    [Input('button', 'n_clicks')]
)
def draw_map(n_clicks):
    return (fig)

app.run_server(debug=True)