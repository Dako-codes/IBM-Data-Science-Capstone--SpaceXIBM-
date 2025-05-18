# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


# Create a dash application
app = dash.Dash(__name__)

LaunchSites = spacex_df['Launch Site'].unique().tolist()
sites = []
sites.append({'label': 'sites', 'values': 'sites'})
for site in LaunchSites:
    sites.append({'label': site, 'values': site})






# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                dcc.Dropdown(id='site_dropdown',
                                options=sites,
                                value = 'ALL',
                                placeholder=' Select a Launch Site',
                                searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload_slider',
                                min=0,
                                max=10000, 
                                step=1000, 
                                marks={0: '0',
                                100: '100'},
                                value=[min_payload, max_payload]),
                                html.Br(),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(site_dropdown):
    filtered_df = spacex_df
    if site_dropdown == 'ALL':
        df = spacex_df[spacex_df['class']== 1]
        fig = px.pie(df, names = 'Launch Site', hole = .3, title = 'Total Success Launches by Site')
        
    else:
        df = spacex_df.loc[spacex_df['Launch Site']== site_dropdown]
        fig = px.pie(df, names = 'class', hole=.3, title = 'Totall Success Launchs for'+ site_dropdown)
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
def get_scatter(site_dropdown, payload_slider):
    if site_dropdown == 'All':
        low, high = payload
        mask = (spacex_df['Payload Mass (kg)']>= low) & (spacex_df['Payload Mass (kg)']<= high)
        fig = px.scatter(
            spacex_df[mask], x="Payload Mass (kg)", y="class",
            color = "Booster Version",
            size = 'Payload Mass (kg)',
            hover_data=['Payload Mass (kg)'])
    else: 
        low, high = payload_slider
        df = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        mask = (df['Payload Mass (kg)']>=low) & (df['Payload Mass (kg)']<=high)
        fig = px.scatter(
            df[mask], x='Payload Mass (kg)', y= 'class', 
            color = 'Booster Version',
            size = 'Payload Mass (kg)',
            hover_data= ['Payload Mass (kg)'])
        return fig    
        
# Run the app
if __name__ == '__main__':
    app.run()
