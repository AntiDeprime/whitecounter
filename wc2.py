#!/usr/bin/env python
# coding: utf-8

# In[33]:


import pandas as pd


# In[39]:


df = pd.read_csv('data.csv', parse_dates=['date'])
df.dropna(subset = ['count'], inplace=True)


# In[221]:


def polar_days(row):
    
    if (row.date.year % 4 == 0):
        return (row.date.dayofyear / 366 * 360)
    else:
        return (row.date.dayofyear / 365 * 360)

import numpy as np
df['polar_date'] = df.apply(lambda row: polar_days(row), axis=1)
df['year'] = pd.Categorical(df.date.dt.year)
df = df.sort_values(['year', 'polar_date'])


# In[222]:


import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[237]:


# fig = px.scatter_polar(df, r="count", theta="polar_date", color="year", symbol="year", log_r=True,
#                        color_discrete_sequence = px.colors.sequential.Viridis,
#                        range_r=[50, 100000], custom_data=[df.date.dt.strftime('%Y-%m-%d'), 'name'])
# # months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
# #           'August', 'September', 'October', 'November', 'December']

# months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
#           'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

# fig.update_layout(
#     template=None,
#     polar = dict(
#         angularaxis = dict(tickvals=[(a*30) for a in range(0, 12)], ticktext=months), 
#         radialaxis = dict(tickvals=[100, 1000, 10000, 50000]),),
#     legend_title='<b> Год </b>'
    

# )
# fig.update_traces(
#    hovertemplate='<b>%{customdata[1]}</b><br>Дата: %{customdata[0]}<br>Численность: %{r}',
# )
# fig.show()


# In[319]:


fig = px.scatter_polar(df, r="year", theta="polar_date", color=np.sqrt(df['count']), size=np.sqrt(df['count']), #symbol="year", log_r=True,
                       color_continuous_scale = px.colors.sequential.Viridis[2:6], 
                       title='Данные Белого Счетчика по протестным акциям в Москве',
                       range_r=[2011, 2020], custom_data=[df.date.dt.strftime('%Y-%m-%d'), 'name', 'count'])
# months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
#           'August', 'September', 'October', 'November', 'December']

months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
          'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

fig.update_layout(
    template=None,
    
    font=dict(
#         family="Courier New, monospace",
        size=14,
#         color="#7f7f7f"
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