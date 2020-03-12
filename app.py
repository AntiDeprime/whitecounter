import wc2

wc2.show_df = wc2.show_df.drop(columns=['Ссылка'])

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_table


app = dash.Dash(
    __name__, external_stylesheets=[
        "https://codepen.io/chriddyp/pen/bWLwgP.css",
         ],
         external_scripts=[
        'https://kit.fontawesome.com/6b0b673ac1.js',
         ]
)
server = app.server

app.title = 'Белый счетчик'

app.layout = html.Div(id='container', children=[
    html.H1(children=['Митинги в Москве по данным Белого счетчика'], id='app-header',),
    dcc.Tabs([
        dcc.Tab(label='График', id='graph', children=[
            dcc.Graph(id="polar_plot", config={'displayModeBar': False}, figure=wc2.fig,
                         style={"height" : "50vw", "width" : "90vw"},),
                         ]),
        
        dcc.Tab(label='Данные', children=[

            dash_table.DataTable(
                data=wc2.show_df.to_dict('records'),
                columns=[{'id': c, 'name': c} for c in wc2.show_df.columns],
                fixed_rows={ 'headers': True, 'data': 0 },

                style_cell = {
                    'font-family': 'PT Sans',
                    'font-size': '1.4rem',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'maxWidth': 0,
                    'textAlign': 'center'
            },
                    style_cell_conditional=[
                    {'if': {'column_id': 'Дата'},
                        'width': '15%',
                        # 'textAlign': 'right',
                        },

                    {'if': {'column_id': 'Численность'},
                        'width': '15%',
                        # 'textAlign': 'right',
                        },
                        

                    # {'if': {'column_id': 'Ссылка'},
                    #         'overflow': 'hidden',
                    #         'textOverflow': 'ellipsis',
                    #         'maxWidth': 0,
                    #         'width': '20%',},

                    {'if': {'column_id': 'Местоположение (начало)'},
                            'width': '25%',},



    ],
                style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }
            ],
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold',
                'textAlign': 'center',
            },

                style_as_list_view=True,                    
                ) ,
            ]),
        ]),


    html.Div([
        html.Br(),
        html.P(['Разработал Алексей Щетинин', 
                    html.Br(),
                    html.A([html.I(className='far fa-envelope')], href='mailto:to@alxy.sh'),
                    ' ',
                    html.A([html.I(className='fab fa-github')], href='https://github.com/AntiDeprime'),
                    ' ',
                    html.A([html.I(className='fab fa-telegram')], href='https://teleg.run/antideprime'),
                    html.Br(),

                ]),

        html.P(['Официальные соцсети Белого счетчика', 
            html.Br(),
            html.A([html.I(className='fab fa-twitter')], href='https://twitter.com/WhiteCounter'),
            ' ',
            html.A([html.I(className='fab fa-facebook')], href='https://facebook.com/WhiteCounter'),
        ]),
        html.I(['обновлено 12 марта 2020']),
    ], id='source',)
])


if (__name__ == '__main__'):
    app.run_server(debug=True)
