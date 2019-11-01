import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import plots  

app = dash.Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)

app.layout = html.Div(
    [
        html.H1("White Counter Protests Data"),
        dcc.Graph(id="graph", style={"width": "100%", "display": "inline-block"}),
        dcc.Graph(id="hist", 
                    style={"width": "100%", "display": "inline-block"},
                    figure=plots.hist, 
            ),
        html.Button('Submit', id='button'),
    ])

@app.callback (
    Output('graph', 'figure'),
    [Input('button', 'n_clicks')]
)
def draw_map(n_clicks):
    return (plots.fig)

app.run_server(debug=True)