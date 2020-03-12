#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd


# In[6]:


df = pd.read_csv('data.csv', parse_dates=['date'])
df.dropna(subset = ['count'], inplace=True)


# In[7]:


def polar_days(row):
    
    if (row.date.year % 4 == 0):
        return (row.date.dayofyear / 366 * 360)
    else:
        return (row.date.dayofyear / 365 * 360)

import numpy as np
df['polar_date'] = df.apply(lambda row: polar_days(row), axis=1)
df['year'] = pd.Categorical(df.date.dt.year)
df = df.sort_values(['year', 'polar_date'])


# In[8]:


import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[9]:


fig = px.scatter_polar(df, r="year", theta="polar_date", color=np.sqrt(df['count']), size=np.sqrt(df['count'] ), #symbol="year", log_r=True, 
                       color_continuous_scale = px.colors.sequential.Viridis[2:6], size_max=30,
#                        title='Данные Белого Счетчика по протестным акциям в Москве',
                       range_r=[2011, 2020], custom_data=[df.date.dt.strftime('%Y-%m-%d'), 'name', 'count'])
# months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
#           'August', 'September', 'October', 'November', 'December']

months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
          'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

fig.update_layout(
    template=None,
    
    font=dict(
        size=18,
    ),
    polar = dict(
        angularaxis = dict(tickvals=[(a*30) for a in range(0, 12)], ticktext=months), 
        radialaxis = dict(tickvals=[2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020],
                          angle = 90,
                          tickangle = 90 # so that tick labels are not upside down
                         ),
    ),
    coloraxis_colorbar=dict(
        title="Численность",
#         thicknessmode="pixels", thickness=50,
#         lenmode="pixels", len=200,
        yanchor="top", y=1,
        ticks="outside",
    tickvals=np.sqrt([1000, 10000, 25000, 50000]),
    ticktext=['1 тыс.', '10 тыс.', '25  тыс.', '50 тыс.'],
    

)
)
fig.update_traces(
   hovertemplate='<b>%{customdata[1]}</b><br>Дата: %{customdata[0]}<br>Численность: %{customdata[2]}',
)
# fig.show()


# In[31]:


df.sort_values(['date'], ascending=False, inplace=True)
show_df = df[['date', 'name', 'count', 'loc', 'link']]

show_df = pd.DataFrame([df['name'], df.date.dt.strftime('%Y-%m-%d'), df['count'], df['loc'], df['link']]).T
show_df.columns = ['Название акции', 'Дата', 'Численность', 'Местоположение (начало)', 'Ссылка']


# In[ ]:




