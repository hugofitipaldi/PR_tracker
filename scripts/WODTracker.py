import pandas as pd

class WODTracker:
    def __init__(self, csv_path='../data/benchmark_wods.csv'):
        self.csv_path = csv_path
        try:
            self.df_wods = pd.read_csv(csv_path)
        except FileNotFoundError:
            columns = ['WOD Name', 'Description', 'Date', 'Time', 'Category', 'Details']
            self.df_wods = pd.DataFrame(columns=columns)
            self.df_wods.to_csv(csv_path, index=False)

    def log_new_wod(self, wod_name, wod_description, wod_date, wod_time, wod_category, wod_details):
        new_data = {
            'WOD Name': wod_name,
            'Description': wod_description,
            'Date': wod_date,
            'Time': wod_time,
            'Category': wod_category,
            'Details': wod_details
        }
        # Append the new row to the DataFrame
        self.df_wods = self.df_wods.append(new_data, ignore_index=True)
        
        # Save the DataFrame back to CSV
        self.df_wods.to_csv(self.csv_path, index=False)
