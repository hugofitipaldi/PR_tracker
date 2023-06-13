import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

class ExerciseTracker:
    def __init__(self, df):
        self.df = df

    def log_exercise(self, name, weight, reps, date=datetime.now().date()):
        new_data = {
            'Exercise': [name],
            'Weight': [weight],
            'Reps': [reps],
            'Date': [pd.to_datetime(date)]  # convert to datetime
        }
        new_df = pd.DataFrame(new_data)
        self.df = pd.concat([self.df, new_df], ignore_index=True)

    def calculate_1rm(self, name):
        exercise_data = self.df[self.df['Exercise'] == name]
        if not exercise_data.empty:
            weight = exercise_data['Weight'].iloc[-1]  # get the latest weight
            reps = exercise_data['Reps'].iloc[-1]  # get the latest reps
            return weight * (1 + (reps / 30))
        else:
            print(f"No data for exercise {name}")
            return None

    def plot_1rm(self, name):
        exercise_data = self.df[self.df['Exercise'] == name]
        if not exercise_data.empty:
            dates = exercise_data['Date']  # Keep dates as datetime objects
            weights = exercise_data['Weight']
            reps = exercise_data['Reps']
            estimated_1rm = weights * (1 + (reps / 30))

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=dates,
                y=estimated_1rm,
                mode='lines+markers',
                name='Estimated 1RM'
            ))

            fig.update_layout(
                title=f'Estimated 1RM for {name} Over Time',
                xaxis_title='Date',
                yaxis_title='Estimated 1RM (kg)',
                xaxis={'tickangle': 45},
                autosize=False,
                width=900,
                height=500
            )
            
            return fig

        else:
            print(f"No data for exercise {name}")
            return None
