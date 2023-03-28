import dash
from dash import html 
from dash import dcc 
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

train = pd.read_csv('/Users/Oswal/Documents/GitHub/Health-Insurance-Cross-Sell-Prediction-/train.csv')


# Define a function to calculate the average response and no-response rates for a given column
def calculate_averages(column):
    avg = train.groupby(column)['Response'].mean().reset_index()
    avg_response = round(avg[avg['Response'] == 1]['Response'].iloc[0], 2)
    avg_no_response = round(avg[avg['Response'] == 0]['Response'].iloc[0], 2)
    return avg_response, avg_no_response

# Create the layout of the app
app.layout = html.Div([
    html.H1('Bivariate Analysis of the Target Variable vs Regressors'),

    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Gender', 'value': 'Gender'},
            {'label': 'Previously Insured', 'value': 'Previously_Insured'},
            {'label': 'Vehicle Age', 'value': 'Vehicle_Age'},
            {'label': 'Vehicle Damage', 'value': 'Vehicle_Damage'},
            {'label': 'Driving License', 'value': 'Driving_License'},
            {'label': 'Age', 'value': 'Age'},
            {'label': 'Region Code', 'value': 'Region_Code'},
            {'label': 'Annual Premium', 'value': 'Annual_Premium'},
            {'label': 'Policy Sales Channel', 'value': 'Policy_Sales_Channel'},
            {'label': 'Vintage', 'value': 'Vintage'}
        ],
        value='Gender',
        style={'width': '50%'}
    ),

    html.Br(),

    dcc.Graph(id='histogram'),

    html.Br(),

    html.Div([
        html.Div(id='avg-response', className='col-md-6'),
        html.Div(id='avg-no-response', className='col-md-6')
    ], className='row')
])

# Define the callback function for the histogram chart and average labels
@app.callback(
    [dash.dependencies.Output('histogram', 'figure'),
     dash.dependencies.Output('avg-response', 'children'),
     dash.dependencies.Output('avg-no-response', 'children')],
    [dash.dependencies.Input('dropdown', 'value')]
)
def update_charts(column):
    # Calculate the averages for the selected column
    avg_response, avg_no_response = calculate_averages(column)

    # Generate the histogram chart
    fig = px.histogram(train, x=column, color='Response', barmode='overlay', nbins=50,
                        template='plotly_dark', labels={'Response': 'Response', column: column})
    fig.update_layout(title_text='Distribution of ' + column + ' by Response',
                      xaxis_title_text=column,
                      yaxis_title_text='Count')

    # Generate the average response and no-response labels
    avg_response_label = html.H3('Average Response for ' + column + ' = ' + str(avg_response))
    avg_no_response_label = html.H3('Average No Response for ' + column + ' = ' + str(avg_no_response))

    return fig, avg_response_label, avg_no_response_label

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8050)
