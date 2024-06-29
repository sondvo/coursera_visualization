import plotly.express as px
from dash import html
from dash import dcc
import dash
import pandas as pd 
import numpy as np 
from dash.dependencies import Input, Output, State
import datetime as dt

import numpy as np
import pandas as pd

import io

URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"
import pandas as pd
data = pd.read_csv(URL)


app = dash.Dash(__name__) 
app.config.suppress_callback_exceptions = True

app.layout = html.Div(
    children=[
        html.H1(
            'This is the main title',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}
        ),
        html.Div([
            html.H2('Report-type:', style={'margin-right': '2em'}),
            dcc.Dropdown(
                id='dropdown-statistics', 
                options=[
                    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
                ],
                placeholder='Select a report type',
                value='Select Statistics',
                style={'margin-right': '2em'}
            ),
            className="mt-4"
        ]),
        html.Div([
            html.H2('Year', style={'margin-right': '2em'}),
            dcc.Dropdown(
                id='select-year', 
                options=[
                    {'label': i, 'value': i}
                    for i in range(1980, 2014)
                ],
                placeholder='Select-year',
                value='Select-year',
                style={'margin-right': '2em'}
            ),
            className="mt-4"
        ]),
        html.Div([
            html.Div(
                id='output-container', 
                # className='flex flex-wrap items-center justify-center'
            ),
        ])
    ]
)

@app.callback(
    Output(component_id='output-container', component_property='children'),
    [
        Input(component_id='dropdown-statistics', component_property='value'), 
        Input(component_id='select-year', component_property='value')
    ]
)

def update_output_container(report_type, input_year):
    if report_type == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]

#Plot 1 Automobile sales fluctuate over Recession Period (year wise) using line chart
        yearly_rec=recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec, 
                x='Year',
                y='Automobile_Sales',
                title="Automobile sales fluctuate over Recession Years"
            )
        )
#Plot 2 Calculate the average number of vehicles sold by vehicle type and represent as a Bar chart
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2  = dcc.Graph(
                figure=px.bar(
                    average_sales,
                    x='Vehicle_Type',
                    y='Automobile_Sales',
                    title="Average number of vehicles sold by vehicle type")
            )

# Plot 3 : Pie chart for total expenditure share by vehicle type during recessions
        exp_rec= recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title="Total expenditure share by vehicle type during recessions"
            )
        )
# Plot 4 Develop a Bar chart for the effect of unemployment rate on vehicle type and sales
        unemp_data= recession_data.groupby(['Vehicle_Type', 'Automobile_Sales'])['unemployment_rate'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x='Automobile_Sales',
                y='Vehicle_Type',
                color='Vehicle_Type',
                labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
                title='Effect of Unemployment Rate on Vehicle Type and Sales'
            )
        )

        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1),html.Div(children=R_chart2)],style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3),html.Div(children=R_chart4)],style={'display': 'flex'})
        ]




    elif (input_year and report_type=='Yearly Statistics') :
        yearly_data = data[data['Year'] == input_year]
                              
# Plot 1 :Yearly Automobile sales using line chart for the whole period.
        yas= data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas))

# Plot 2 :Total Monthly Automobile sales using line chart.
        mas=data.groupby('Month').sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas,
                x='Month',
                y='Automobile_Sales',
                title='Total Monthly Automobile Sales'
            )
        )
# Plot bar chart for average number of vehicles sold during the given year
        avr_vdata=yearly_data.groupby('Month')['Automobile_Sales'].mean()
        Y_chart3 = dcc.Graph( 
            figure=px.bar(
                avr_vdata,
                title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)
            )
        )
# Plot 4 Total Advertisement Expenditure for each vehicle using pie chart
          # grouping data for plotting.
          # Hint:Use the columns Vehicle_Type and Advertising_Expenditure
        exp_data=yearly_data.groupby('Vehicle_Type').sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data, 
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Total Advertisment Expenditure for Each Vehicle'
            ))
        return [
                html.Div(className='chart-item', children=[html.Div(children=Y_chart1),html.Div(children=Y_chart2)],style={'display':'flex'}),
                html.Div(className='chart-item', children=[html.Div(children=Y_chart3),html.Div(children=Y_chart4)],style={'display': 'flex'})
            ]


if __name__ == '__main__':
    app.run_server()