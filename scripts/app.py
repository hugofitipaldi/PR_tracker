import webbrowser
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from ExerciseTracker import ExerciseTracker 
import pandas as pd

df = pd.read_csv('../data/exercise_log.csv')
tracker = ExerciseTracker(df)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Exercise Tracker'),
    dcc.Input(id='exercise-name', type='text', placeholder='Enter exercise name'),
    dcc.Input(id='weight', type='number', placeholder='Enter weight'),
    dcc.Input(id='reps', type='number', placeholder='Enter reps'),
    dcc.Input(id='date', type='text', placeholder='Enter date (YYYY-MM-DD)'),
    html.Button('Submit', id='submit', n_clicks=0),
    html.Div(id='output'),
    dcc.Graph(id='graph', figure={}),  # empty graph
    html.Button('Save Data', id='save-button', n_clicks=0),  # save data button
    html.Div(id='save-output')  # output for the save data button
])

@app.callback(
    Output('output', 'children'),
    Output('graph', 'figure'),
    Input('submit', 'n_clicks'),
    State('exercise-name', 'value'),
    State('weight', 'value'),
    State('reps', 'value'),
    State('date', 'value'),
)
def update_output(n_clicks, exercise_name, weight, reps, date):
    if n_clicks > 0:
        tracker.log_exercise(exercise_name, weight, reps, date)
        estimated_1rm = tracker.calculate_1rm(exercise_name)
        figure = tracker.plot_1rm(exercise_name)
        return f"The estimated 1RM for {exercise_name} is {estimated_1rm} kg", figure
    return dash.no_update, dash.no_update

@app.callback(
    Output('save-output', 'children'),
    Input('save-button', 'n_clicks'),
)

def save_data(n):
    if n > 0:  # if button is clicked
        # Button has been clicked, save the data
        tracker.df.to_csv('../data/exercise_log.csv', index=False)
        return "Data Saved!"
    return ""  # no message if button has not been clicked


if __name__ == '__main__':
    # Open a new browser tab automatically when the script is run
    webbrowser.open_new_tab('http://localhost:8050')
    app.run_server(debug=False, host='127.0.0.1', port=8050)

