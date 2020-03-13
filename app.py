# import graph and table
import wc2

# import Dash components 
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_table

# Dash app configuration 
app = dash.Dash(
    __name__, external_stylesheets=[
        # appearance 
        "https://codepen.io/chriddyp/pen/bWLwgP.css",
         ],
        # social icons
         external_scripts=[
        'https://kit.fontawesome.com/6b0b673ac1.js',
         ]
)
server = app.server
app.title = 'White Counter'

# App layout
app.layout = html.Div(id='container', children=[
    # Header
    html.H1(children=['Protests in Moscow, White Counter Historical Data'], id='app-header',),
    # Tabs 
    dcc.Tabs([
        # Graph tab
        dcc.Tab(label='Plot', id='graph', children=[
            dcc.Graph(id="polar_plot", config={'displayModeBar': False}, figure=wc2.fig,),
        ]),
        
        # Data Table
        dcc.Tab(label='Data Table', children=[

            dash_table.DataTable(
                # loading data 
                data=wc2.show_df.to_dict('records'),
                columns=[{'id': c, 'name': c} for c in wc2.show_df.columns],
                # fixed header
                fixed_rows={ 'headers': True, 'data': 0 },
                
                # font, wrapping, align
                style_cell = {
                    'font-family': 'PT Sans',
                    'font-size': '1.4rem',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'maxWidth': 0,
                    'textAlign': 'center'},
                
                # widths 
                style_cell_conditional=[
                    {'if': {'column_id': 'Date'},
                        'width': '15%',},
                    {'if': {'column_id': 'Attendance'},
                        'width': '15%',},
                    {'if': {'column_id': 'Location'},
                        'width': '35%',},
                ],
                
                # odd rows grey
                style_data_conditional=[
                    {'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'}
                ],
                
                # format header 
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold',
                    'textAlign': 'center',
                },
                
                # no vertical borders 
                style_as_list_view=True,        
                
                ) ,
            ]),
        ]),


    html.Div([
        html.Br(),
        html.P(['Developed by Aleksei Shchetinin', 
                    html.Br(),
                    html.A([html.I(className='far fa-envelope')], href='mailto:to@alxy.sh'),
                    ' ',
                    html.A([html.I(className='fab fa-github')], href='https://github.com/AntiDeprime'),
                    ' ',
                    html.A([html.I(className='fab fa-telegram')], href='https://t.me/antideprime'),
                    html.Br(),

                ]),

        html.P(['White Counter NGO', 
            html.Br(),
            html.A([html.I(className='fab fa-twitter')], href='https://twitter.com/WhiteCounter'),
            ' ',
            html.A([html.I(className='fab fa-facebook')], href='https://facebook.com/WhiteCounter'),
        ]),
        html.I(['Last update: 2020/03/12']),
    ], id='source',)
])


if (__name__ == '__main__'):
    app.run_server(debug=True)
