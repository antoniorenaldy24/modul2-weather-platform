import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px

# Load dataset
url = 'https://raw.githubusercontent.com/plotly/datasets/master/diabetes.csv'
df = pd.read_csv(url)

# Create a Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div(children=[
    html.H1(children='Dashboard Data Visualization'),
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': '0 - No Diabetes', 'value': 0},
            {'label': '1 - Diabetes', 'value': 1}
        ],
        value=0
    ),
    dcc.Graph(
        id='example-graph'
    )
])

@app.callback(
    Output('example-graph', 'figure'),
    [Input('dropdown', 'value')]
)
def update_figure(selected_value):
    filtered_df = df[df['Outcome'] == selected_value]
    fig = px.scatter(
        filtered_df, 
        x='BMI', 
        y='Glucose', 
        color='Outcome', 
        title='Diabetes Data Visualization'
    )
    return fig

if __name__ == '__main__':
    # Menggunakan port 8052 agar tidak bentrok dengan System Alpha (8050)
    app.run(debug=False, host='127.0.0.1', port=8052)
