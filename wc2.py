import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class WCAppData(object):
    '''Performs data loading and processing,
       Builds plot and data table'''

    def __init__(self):
        # set month names
        self.months = ['January', 'February', 'March',
                       'April', 'May', 'June', 'July',
                       'August', 'September', 'October',
                       'November', 'December']
        #set color scheme
        self.colors = px.colors.sequential.Viridis[2:6]
        #load data 
        self.load_data('data.csv')

    def __polar_days__(self, row):
        '''Distributes dates evenly across 360 degrees'''
        if (row.date.year % 4 == 0):
            return (row.date.dayofyear / 366 * 360)
        else:
            return (row.date.dayofyear / 365 * 360)

    def load_data(self, path):
        '''Loads data frame'''
        self.df = pd\
            .read_csv(path, parse_dates=['date'])\
            .dropna(subset=['count'])\
            .sort_values(['date'], ascending=False)
        
        # make evenly distributed dates
        self.df['polar_date'] = self.df.apply(
            lambda row: self.__polar_days__(row), axis=1)
        
        self.df['year'] = pd.Categorical(self.df.date.dt.year)
        # format dates
        self.df['date'] = self.df.date.dt.strftime('%Y-%m-%d')
        # make counts whole numbers
        self.df['count'] = self.df['count'].astype(int)

    def build_scatter(self):
        '''Builds scatter polar plot'''
        fig = px.scatter_polar(
            self.df,
            r="year",
            theta="polar_date",
            color=np.sqrt(self.df['count']),
            size=np.sqrt(self.df['count']),
            color_continuous_scale=self.colors,
            size_max=30, # appearance
            range_r=[2011, 2020],  # appearance
            custom_data=['date', 'name', 'count'])  # for hover

        fig.update_layout(

            template=None,
            font=dict(size=18,),

            # format axes
            polar=dict(angularaxis=dict(
                tickvals=[(a*30) for a in range(0, 12)],
                ticktext=self.months),
                radialaxis=dict(
                tickvals=[2013, 2014, 2015, 2016,
                          2017, 2018, 2019, 2020],
                angle=90,
                tickangle=90,),),

            # format colorbar
            coloraxis_colorbar=dict(
                title='Attendance',
                ticks="outside",
                tickvals=np.sqrt([1000, 10000, 25000, 50000]),
                ticktext=['1k', '10k', '25k', '50k'],),)

        # format hover
        fig.update_traces(
            hovertemplate=('<b>%{customdata[1]}</b><br>'
                           'Date: %{customdata[0]}<br>'
                           'Attendance: %{customdata[2]}'),)
        return(fig)

    def build_data_table(self):
        '''Builds a table to show in the app'''
        out = self.df[['name', 'date', 'count', 'loc']].copy()
        out.columns = ['Name', 'Date', 'Attendance', 'Location']
        return(out)