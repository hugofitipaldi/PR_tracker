import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

class ExerciseTracker:
    """
    A class to track and analyze exercise performance over time.
    
    This tracker logs exercises with their names, weights lifted, repetitions (reps),
    and dates. It can calculate the one-repetition maximum (1RM) for a given exercise
    based on the most recent performance and plot the progression of the 1RM and actual
    weights lifted over time.
    
    Attributes:
        df (pd.DataFrame): A pandas DataFrame containing the log of exercises. Each row
                           records an exercise, its weight, reps, and the date it was performed.
    """
    def __init__(self, df):
        """
        Initializes the ExerciseTracker with an existing DataFrame.
        
        Parameters:
            df (pd.DataFrame): A pandas DataFrame to initialize the tracker. Expected
                               columns are 'Exercise', 'Weight', 'Reps', and 'Date'.
        """
        self.df = df

    def log_exercise(self, name, weight, reps, date=datetime.now().date()):
        """
        Logs a new exercise entry into the tracker.
        
        Parameters:
            name (str): The name of the exercise.
            weight (float): The weight lifted in kilograms.
            reps (int): The number of repetitions performed.
            date (datetime.date, optional): The date the exercise was performed. Defaults to the current date.
        """
        new_data = {
            'Exercise': [name],
            'Weight': [weight],
            'Reps': [reps],
            'Date': [pd.to_datetime(date)]  # convert to datetime
        }
        new_df = pd.DataFrame(new_data)
        self.df = pd.concat([self.df, new_df], ignore_index=True)

    def calculate_1rm(self, name):
        """
        Calculates the estimated one-repetition maximum (1RM) for the specified exercise
        based on the most recent performance.
        
        The formula used is: 1RM = Weight * (1 + (Reps / 30)).
        
        Parameters:
            name (str): The name of the exercise to calculate 1RM for.
        
        Returns:
            float or None: The estimated 1RM if data exists for the given exercise, else None.
        """
        exercise_data = self.df[self.df['Exercise'] == name]
        if not exercise_data.empty:
            weight = exercise_data['Weight'].iloc[-1]  # get the latest weight
            reps = exercise_data['Reps'].iloc[-1]  # get the latest reps
            return weight * (1 + (reps / 30))
        else:
            print(f"No data for exercise {name}")
            return None

    def plot_1rm(self, name):
        """
        Plots the progression of the estimated 1RM and actual weights lifted for the specified
        exercise over time.
        
        Parameters:
            name (str): The name of the exercise to plot 1RM progression for.
        
        Returns:
            go.Figure or None: A Plotly figure showing the estimated 1RM and weight progression
                               over time if data exists for the given exercise, else None.
        """
        exercise_data = self.df[self.df['Exercise'] == name]
        if not exercise_data.empty:
            dates = exercise_data['Date']  # Keep dates as datetime objects
            weights = exercise_data['Weight']
            reps = exercise_data['Reps']
            estimated_1rm = weights * (1 + (reps / 30))

            fig = go.Figure()
            
            #Plot estimated 1RM as a dashed red line
            fig.add_trace(go.Scatter(
                x=dates,
                y=estimated_1rm,
                mode='lines+markers',
                name='Estimated 1RM',
                line=dict(color='red', dash='dash')
                ))
            
            # Plot actual weight as a solid blue line
            fig.add_trace(go.Scatter(
                x=dates,
                y=weights,
                mode='lines+markers',
                name='Weight',
                line=dict(color='blue', dash='solid')
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
