import pandas as pd
import plotly_express as px
from datetime import datetime
import plotly.graph_objs as go 
import numpy as np

#url = 'https://raw.githubusercontent.com/AntiDeprime/whitecounter/master/data.csv'
df = pd.read_csv('./data.csv', parse_dates=['date'], usecols=['date', 'name', 'count', 'coord'])
df.dropna(inplace=True)
df['selected'] = True

df[['lat', 'lon']] = df['coord'].str.split(', ' ,expand=True).astype('float')
#df.sort_values(by=['date'], ascending=False)
#df['date_str'] = df['date'].dt.strftime('%Y-%m-%d')
# df1 = df.set_index('date')
# df['Q'] = df.date.dt.quarter
# df['M'] = df.date.dt.month
# df['D'] = df.date.dt.dayofyear
# df['Y'] = df.date.dt.year


def days_diff(sd, ed):
  """Days between two dates"""
  return (ed - sd) / np.timedelta64(1,'D')

start_date = df['date'].min()
end_date = df['date'].max()

total_days = days_diff(start_date, end_date)

jan1_13_19 = pd.date_range(start='2013-01-01', end='2019-01-01', freq='YS')

dates = {}
for year in jan1_13_19:
    y = str(year.year)
    d = int(days_diff(start_date, year))
    dates[y]=d

df['days_from'] = days_diff(start_date, df['date'])

def mask_dates(rng):
  df['selected'] = df['days_from'].between(rng[0],rng[1])
  df['colors'] = df['selected'].astype('category')
  df.sort_values(by=['selected'], ascending=False, inplace=True)



token = 'pk.eyJ1IjoiYW50aWRlcHJpbWUiLCJhIjoiY2syYzBwdXVxMDl3eDNicW9pbTE2dzJ5MCJ9.3_OL4GUnwOryXefKh73ZVw'
px.set_mapbox_access_token(token)

           

# df_q_sum = df1.resample('Q').sum().reset_index()
# df_q_count = df1.resample('Q').count().reset_index()

# hist = px.line(df_q_sum, 
#                 x="date", 
#                 y='count', 
#                 line_shape="spline",)

# hist.layout.height = 200








import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

#import plots  

app = dash.Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)

app.layout = html.Div([

    html.Div(
        [
            html.H1(["White Counter Protests Data"], id='h1', style={"width": '75%', "display": "inline-block", 'textAlign': 'center'},),

            dcc.Graph(id="graph", 
                        style={"width": '75%', "display": "inline-block", 'textAlign': 'center'},
                        config={'displayModeBar': False}),

            dcc.Graph(id="timeline", 
                        style={"width": '75%', "display": "inline-block", 'textAlign': 'center'},
                        config={'displayModeBar': False},),

            html.Div([        
                dcc.RangeSlider(
                    id='date_range',
                    min=0,
                    max=int(total_days),
                    marks={
                        dates['2014']: {'label': '2014'},
                        dates['2015']: {'label': '2015'},
                        dates['2016']: {'label': '2016'},
                        dates['2017']: {'label': '2017'},
                        dates['2018']: {'label': '2018'},
                        dates['2019']: {'label': '2019'},
                        },
                    value=[0, int(total_days)
                        ])
                    ], 
                    style={"width": '60%', "display": "inline-block", 'textAlign': 'center'},
                    ),


            # dcc.Graph(id="hist", 
            #             style={"width": "100%", "display": "inline-block"},
            #             figure=hist, 
            #     ),

        ], style={
                    #   "display": "flex",
                    #   "flex-direction": "row",
                    #   "flex-wrap": "wrap",
                    #   #"flex": "0 0 800",
                    #   "flex-basis": "90%",
                    #   #"justify-content": "center",
                    #   #"align-items": "stretch",
                    #"width": "75%",
                    'textAlign': 'center'
    }),
    html.Div([
        dcc.Markdown(id='summary')
    ], style={"width": 400,})
                    
                  
                  
], style={
                    "display": "flex",
                    "flex-direction": "row",
                    #   "flex-wrap": "wrap",
                    "flex": "0 1 800",
                    #"flex-basis": "90%",
                    "justify-content": "center",
                    "align-items": "center",
                    "width": "75%",

}

)
@app.callback (
    Output('graph', 'figure'),
    [Input('date_range', 'value')]
)
def draw_map(value):
    mask_dates(value)
    fig = px.scatter_mapbox(df[df['selected']],
                        lat="lat", 
                        lon="lon",  
                        #color="days_from", 
                        size="count",
                        #color_continuous_scale=px.colors.sequential.Burg, 
                        size_max=20, 
                        zoom=9, 
                        height=400, 
                        #animation_frame='date_str',  
                        color_discrete_sequence=['rgba(32, 73, 105, 0.5)']
                        )
    
    fig.layout.margin=go.layout.Margin(l=32,r=0,b=0,t=0,pad=0)  
    try:     
        fig.layout.showscale=False
    except:
        pass
    return (fig)


@app.callback (
    Output('timeline', 'figure'),
    [Input('date_range', 'value')]
)
def draw_timeline(value):
    mask_dates(value)


    timeline = px.scatter(df, x='date', y='count',
                            color='colors', height=100, hover_name='name',
                            color_discrete_sequence=['rgba(32, 73, 105, 1)', 'rgba(218, 218, 218, 1)']) 

    timeline.layout.margin = go.layout.Margin(l=0,r=0,b=0,t=0,pad=0)        
    timeline.layout.xaxis.title = None
    timeline.layout.yaxis.title = None
    timeline.layout.xaxis.showticklabels = False
    timeline.layout.yaxis.ticklabelalignment: 'inside'
    timeline.layout.font.size = 18 # Размер шрифта
    timeline.layout.template = 'plotly_white'
    #timeline.layout.clickmode = 'select'
    timeline.update_layout(showlegend=False)
    return (timeline)

@app.callback (
    Output('summary', 'children'),
    [Input('date_range', 'value')]
)
def compose_text(value):
    mask_dates(value)
    masked_df = df[df['selected']]
    beg_date = pd.to_datetime(masked_df['date'].min()).strftime("%b-%d-%Y")
    end_date = pd.to_datetime(masked_df['date'].max()).strftime("%b-%d-%Y")
    total_count = int(masked_df['count'].sum())
    total_protests = masked_df['count'].count()
    return(f"""
        ## Summary

        *{beg_date} to {end_date}*

        **Total count:** {total_count}  
        **Total protests:** {total_protests}
        """)






app.run_server(debug=True)