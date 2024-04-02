import webbrowser
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from ExerciseTracker import ExerciseTracker 
from WODTracker import WODTracker
import pandas as pd

df = pd.read_csv('../data/exercise_log.csv')
tracker = ExerciseTracker(df)

wod_tracker = WODTracker()


exercise_options = [
    {'label': 'Front Squat', 'value': 'Front Squat'},
    {'label': 'Snatch', 'value': 'Snatch'},
    {'label': 'Back Squat', 'value': 'Back Squat'},
    {'label': 'Power Snatch', 'value': 'Power Snatch'},
    {'label': 'Deadlift', 'value': 'Deadlift'},
    {'label': 'Power Clean', 'value': 'Power Clean'},
    {'label': 'Clean and Jerk', 'value': 'Clean and Jerk'},
    {'label': 'Push Jerk', 'value': 'Push Jerk'},
    {'label': 'Split Jerk', 'value': 'Split Jerk'},
    {'label': 'Bench Press', 'value': 'Bench Press'},
    {'label': 'Hang Snatch', 'value': 'Hang Snatch'},
    {'label': 'Overhead Squat', 'value': 'Overhead Squat'},
    {'label': 'Push Press', 'value': 'Push Press'},
    {'label': 'Hang Clean', 'value': 'Hang Clean'},
    {'label': 'Clean', 'value': 'Clean'},
    {'label': 'Strict Press', 'value': 'Strict Press'}
]


#app = dash.Dash(__name__)
# Flatly theme CDN
JOURNAL = dbc.themes.JOURNAL

app = dash.Dash(__name__, external_stylesheets=[JOURNAL])

# Define CSS styles
styles = {
    'container': {
        'width': '80%',
        'margin': '0 auto',
        'padding': '20px'
    },
    'tab': {
        'padding': '20px'
    },
    'button': {
        'margin-top': '10px',
    },
    'save-button_st': {
        'margin-top': '10px',
        'display': 'inline-block', 
        "marginLeft": "80%",
        "width": "10%",
        "height": "10%",
    },
    'output': {
        'margin-top': '20px'
    },
    'graph': {
        'width': '100%',
        'height': '400px'
    }
}

app.layout = html.Div(
    style=styles['container'],  # Apply container style
    children=[
        html.H1('Exercise Tracker'),
        dcc.Tabs(
            style=styles['tab'],  # Apply tab style
            children=[
                dcc.Tab(
                    label='Log Exercise',
                    children=[
                        html.Div(
                            style=styles['tab'],  # Apply tab style
                            children=[
                                dcc.Dropdown(
                                    id='exercise-name',
                                    options=exercise_options,
                                    placeholder='Select exercise',
                                    style=styles['button']  # Apply button style
                                ),
                                dcc.Input(
                                    id='weight',
                                    type='number',
                                    placeholder='Enter weight',
                                    style=styles['button']  # Apply button style
                                ),
                                dcc.Input(
                                    id='reps',
                                    type='number',
                                    placeholder='Enter reps',
                                    style=styles['button']  # Apply button style
                                ),
                                dcc.Input(
                                    id='date',
                                    type='text',
                                    placeholder='Enter date (YYYY-MM-DD)',
                                    style=styles['button']  # Apply button style
                                ),
                                html.Button(
                                    'Submit',
                                    id='submit',
                                    n_clicks=0,
                                    style=styles['button']  # Apply button style
                                ),
                                html.Div(id='output', style=styles['output']),  # Apply output style
                                dcc.Graph(id='log-graph', style=styles['graph'])  # Apply graph style
                            ]
                        ),
                        html.Button(
                            'Save Data',
                            id='save-button',
                            n_clicks=0,
                            style=styles['save-button_st']  # Apply button style
                        ),
                        html.Div(id='save-output', style=styles['output'])  # Apply output style
                    ]
                ),
                dcc.Tab(
                    label='Predicted 1RM',
                    children=[
                        html.Div(
                            style=styles['tab'],  # Apply tab style
                            children=[
                                dcc.Dropdown(
                                    id='exercise-prediction',
                                    options=exercise_options,
                                    placeholder='Select exercise',
                                    style=styles['button']  # Apply button style
                                ),
                                html.Button(
                                    'Create Plot',
                                    id='plot-button',
                                    n_clicks=0,
                                    style=styles['button']  # Apply button style
                                ),
                                dcc.Graph(
                                    id='prediction-graph',
                                    style=styles['graph']  # Apply graph style
                                )
                            ]
                        )
                    ]
                ),
                dcc.Tab(
                    label='Benchmark WODs',
                    children=[
                        html.Div(
                            style=styles['tab'],
                            children=[
                                dcc.Input(
                                    id='wod-name',
                                    type='text',
                                    placeholder='Enter WOD name',
                                    style=styles['button']
                                ),
                                dcc.Textarea(
                                    id='wod-description',
                                    placeholder='Enter WOD description',
                                    style={'width': '100%', 'height': 100, **styles['button']}
                                ),
                                dcc.Input(
                                    id='wod-date',
                                    type='text',
                                    placeholder='Enter date (YYYY-MM-DD)',
                                    style=styles['button']
                                ),
                                dcc.Input(
                                    id='wod-time',
                                    type='text',
                                    placeholder='Enter completion time (MM:SS)',
                                    style=styles['button']
                                ),
                                dcc.Dropdown(
                                    id='wod-category',
                                    options=[
                                        {'label': 'Scaled', 'value': 'Scaled'},
                                        {'label': 'Rx', 'value': 'Rx'},
                                        {'label': 'Rx+', 'value': 'Rx+'}
                                    ],
                                    placeholder='Select category',
                                    style=styles['button']
                                ),
                                dcc.Input(
                                    id='wod-scale-detail',
                                    type='text',
                                    placeholder='Details on Scaled/Rx+ if applicable',
                                    style=styles['button']
                                ),
                                html.Button(
                                    'Log WOD',
                                    id='log-wod-button',
                                    n_clicks=0,
                                    style=styles['button']
                                ),
                                html.Div(id='log-wod-output', style=styles['output'])
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)


# Log Exercise callback
@app.callback(
    Output('output', 'children'),
    Output('log-graph', 'figure'),
    Input('submit', 'n_clicks'),
    State('exercise-name', 'value'),
    State('weight', 'value'),
    State('reps', 'value'),
    State('date', 'value'),
)

def log_exercise(n_clicks, exercise_name, weight, reps, date):
    if n_clicks > 0:
        tracker.log_exercise(exercise_name, weight, reps, date)
        estimated_1rm = tracker.calculate_1rm(exercise_name)
        figure = tracker.plot_1rm(exercise_name)
        return f"The estimated 1RM for {exercise_name} is {estimated_1rm} kg", figure
    return dash.no_update, dash.no_update

# Save Data callback
@app.callback(
    Output('save-output', 'children'),
    Input('save-button', 'n_clicks')
)
def save_data(n_clicks):
    if n_clicks > 0:
        tracker.df.to_csv('../data/exercise_log.csv', index=False)
        return "Data Saved!"
    return ""

# Predicted 1RM callback
@app.callback(
    Output('prediction-graph', 'figure'),
    Input('plot-button', 'n_clicks'),
    State('exercise-prediction', 'value')
)
def plot_prediction(n_clicks, exercise_name):
    if n_clicks > 0:
        figure = tracker.plot_1rm(exercise_name)
        return figure
    return dash.no_update

# Benchmark WODs callback
@app.callback(
    Output('log-wod-output', 'children'),
    Input('log-wod-button', 'n_clicks'),
    State('wod-name', 'value'),
    State('wod-description', 'value'),
    State('wod-date', 'value'),
    State('wod-time', 'value'),
    State('wod-category', 'value'),
    State('wod-scale-detail', 'value'),
)
def log_benchmark_wod(n_clicks, wod_name, wod_description, wod_date, wod_time, wod_category, wod_scale_detail):
    if n_clicks > 0:
        wod_tracker.log_new_wod(wod_name, wod_description, wod_date, wod_time, wod_category, wod_scale_detail)
        return f"WOD '{wod_name}' logged successfully."
    return dash.no_update

if __name__ == '__main__':
    # Open a new browser tab automatically when the script is run
    webbrowser.open_new_tab('http://localhost:8050')
    app.run_server(debug=False, host='127.0.0.1', port=8050)
