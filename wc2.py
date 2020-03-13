#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[8]:


df = pd.read_csv('data.csv', parse_dates=['date'])
df.dropna(subset = ['count'], inplace=True)


# In[9]:


# Distribute years evenly across 360 degrees 
def polar_days(row):
    if (row.date.year % 4 == 0):
        return (row.date.dayofyear / 366 * 360)
    else:
        return (row.date.dayofyear / 365 * 360)

df['polar_date'] = df.apply(lambda row: polar_days(row), axis=1)
df['year'] = pd.Categorical(df.date.dt.year)
df = df.sort_values(['year', 'polar_date'])


# In[10]:


# Build scatter polar plot 

fig = px.scatter_polar(df, r="year", theta="polar_date", # data
                       color=np.sqrt(df['count']), size=np.sqrt(df['count']), #size and color 
                       color_continuous_scale = px.colors.sequential.Viridis[2:6],size_max=30, # appearance 
                       range_r=[2011, 2020],  # appearance 
                       custom_data=[df.date.dt.strftime('%Y-%m-%d'), 'name', 'count']) # for hover 

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December'] 


fig.update_layout(
    template=None,
    # font size
    font=dict(size=18,),
    
    # format axes
    polar = dict(
        angularaxis = dict(tickvals=[(a*30) for a in range(0, 12)], ticktext=months), 
        radialaxis = dict(tickvals=[2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020],
                          angle = 90,
                          tickangle = 90,),
    ),
    
    # format colorbar 
    coloraxis_colorbar=dict(
        title='Attendance',
        ticks="outside",
        tickvals=np.sqrt([1000, 10000, 25000, 50000]),
        ticktext=['1k', '10k', '25k', '50k'],  
    ),
)

# format hover 
fig.update_traces(
    hovertemplate='<b>%{customdata[1]}</b><br>Date: %{customdata[0]}<br>Attendance: %{customdata[2]}',
)


# In[11]:


# creating data table 
# sorting descending by date 
df.sort_values(['date'], ascending=False, inplace=True)

show_df = df[['date', 'name', 'count', 'loc']]

show_df = pd.DataFrame([df['name'], df.date.dt.strftime('%Y-%m-%d'), df['count'], df['loc']]).T
show_df.columns = ['Name', 'Date', 'Attendance', 'Location']


# In[ ]:




