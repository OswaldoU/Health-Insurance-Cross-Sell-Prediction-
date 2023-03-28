import plotly.graph_objs as go
import plotly.express as px
import pandas as pd


train = pd.read_csv('/Users/Oswal/Documents/GitHub/Health-Insurance-Cross-Sell-Prediction-/train.csv')

def plot_charts(column):
    fig = px.histogram(train, x=column, color="Response", nbins=50, barmode="overlay", template="plotly_dark",
                       labels={'Response': 'Response', column: column})
    fig.update_layout(title_text="Distribution of " + column + " by Response",
                      xaxis_title_text=column,
                      yaxis_title_text="Count")
    return fig

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Bivariate Analysis of the Target Variable vs Regressors"),

    html.Div([
        dcc.Graph(id='chart1', figure=plot_charts('Gender')),
        dcc.Graph(id='chart2', figure=plot_charts('Previously_Insured')),
        dcc.Graph(id='chart3', figure=plot_charts('Vehicle_Age')),
        dcc.Graph(id='chart4', figure=plot_charts('Vehicle_Damage')),
        dcc.Graph(id='chart5', figure=plot_charts('Driving_License')),
        dcc.Graph(id='chart6', figure=plot_charts('Age')),
        dcc.Graph(id='chart7', figure=plot_charts('Region_Code')),
        dcc.Graph(id='chart8', figure=plot_charts('Annual_Premium')),
        dcc.Graph(id='chart9', figure=plot_charts('Policy_Sales_Channel')),
        dcc.Graph(id='chart10', figure=plot_charts('Vintage'))
    ], className='row')
])


if __name__ == '__main__':
    app.run_server(debug=True)
