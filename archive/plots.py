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


token = 'pk.eyJ1IjoiYW50aWRlcHJpbWUiLCJhIjoiY2syYzBwdXVxMDl3eDNicW9pbTE2dzJ5MCJ9.3_OL4GUnwOryXefKh73ZVw'
px.set_mapbox_access_token(token)


fig = px.scatter_mapbox(df[df['selected']],
                        lat="lat", 
                        lon="lon",  
                        #color="count", 
                        size="count",
                        #color_continuous_scale=px.colors.cyclical.IceFire, 
                        size_max=15, 
                        zoom=10, 
                        #animation_frame='date_str',  
                        )

fig.layout.margin=go.layout.Margin(l=32,r=0,b=0,t=0,pad=0)                  

# df_q_sum = df1.resample('Q').sum().reset_index()
# df_q_count = df1.resample('Q').count().reset_index()

# hist = px.line(df_q_sum, 
#                 x="date", 
#                 y='count', 
#                 line_shape="spline",)

# hist.layout.height = 200

timeline = px.scatter(df[df['selected']], x='date', y='count', hover_name='name', height=200) 

timeline.layout.margin = go.layout.Margin(l=0,r=0,b=0,t=0,pad=0)        
timeline.layout.xaxis.title = None
timeline.layout.yaxis.title = None
timeline.layout.xaxis.showticklabels = False
timeline.layout.yaxis.ticklabelalignment: 'inside'
timeline.layout.font.size = 18 # Размер шрифта