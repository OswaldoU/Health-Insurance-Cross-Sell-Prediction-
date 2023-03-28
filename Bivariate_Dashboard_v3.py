import pandas as pd
import plotly.express as px
import dash
from dash import html 
from dash import dcc 

# Load the data
train = pd.read_csv('train.csv')

# Calculate the unique values for the dropdown list
options = [{'label': x, 'value': x} for x in train.columns]

# Define the app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1('Bivariate Analysis Dashboard'),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='dropdown',
                options=options,
                value='Gender'
            )
        ], className='three columns'),
        html.Div([
            html.H3('Average Response Rate by Selected Variable'),
            html.Div([
                html.Div([
                    html.H6('Response'),
                    html.H3(id='avg-response', style={'color': 'green'})
                ], className='three columns'),
                html.Div([
                    html.H6('No Response'),
                    html.H3(id='avg-no-response', style={'color': 'red'})
                ], className='three columns')
            ], className='row')
        ], className='nine columns')
    ], className='row'),
    html.Div([
        dcc.Graph(id='histogram')
    ], className='row')
])

# Define the calculate_averages function
def calculate_averages(column):
    counts = train.groupby(column)['Response'].value_counts().unstack().fillna(0)
    total = counts.sum(axis=1)
    response = counts[1]
    proportion = (response / total).round(2)
    return proportion

# Define the update_charts function
@app.callback(
    [dash.dependencies.Output('histogram', 'figure'),
     dash.dependencies.Output('avg-response', 'children'),
     dash.dependencies.Output('avg-no-response', 'children')],
    [dash.dependencies.Input('dropdown', 'value')]
)
def update_charts(column):
    # Calculate the averages for the selected column
    proportions = calculate_averages(column)

    # Generate the histogram chart
    fig = px.histogram(train, x=column, color='Response', barmode='overlay', nbins=50,
                        template='plotly_dark', labels={'Response': 'Response', column: column})
    fig.update_layout(title_text='Distribution of ' + column + ' by Response',
                      xaxis_title_text=column,
                      yaxis_title_text='Count')

    # Generate the average response and no-response labels
    avg_response_label = html.H3('Proportion of Responses for ' + column + ': ' + str(proportions[1]))
    avg_no_response_label = html.H3('Proportion of No Responses for ' + column + ': ' + str(proportions[0]))

    return fig, avg_response_label, avg_no_response_label

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8050)