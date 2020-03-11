import wc2

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_table


app = dash.Dash(
    __name__, external_stylesheets=[
        "https://codepen.io/chriddyp/pen/bWLwgP.css",
         ]
)
server = app.server

app.title = 'Белый счетчик'

app.layout = html.Div(id='container',children=[
    dcc.Tabs([
        dcc.Tab(label='График', children=[
            dcc.Graph(id="polar_plot", config={'displayModeBar': False}, figure=wc2.fig),]),
        
        dcc.Tab(label='Данные', children=[

            dash_table.DataTable(
                data=wc2.df.to_dict('records'),
                columns=[{'id': c, 'name': c} for c in wc2.df.columns],
                fixed_rows={ 'headers': True, 'data': 0 },

                style_cell = {
                    'font-family': 'PT Sans',
                    'font-size': '1.4rem',
            },

                style_table={
                    'maxHeight': '300px',
                    # 'overflowY': 'scroll',
                    'overflowY': 'auto',
                    
                    },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    }
                ],
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                }                       
                ) ,
            ]),
        ]),


    html.Div([dcc.Markdown('На данных белого счетчика')], id='source'),] )


if (__name__ == '__main__'):
    app.run_server(debug=True)
