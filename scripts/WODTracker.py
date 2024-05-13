import pandas as pd

class WODTracker:
    """
    A class to track workout of the day (WOD) records using a CSV file as a data store.

    Attributes:
        csv_path (str): The file path to the CSV file where WOD records are stored.
        df_wods (DataFrame): A pandas DataFrame containing the WOD records.

    Methods:
        log_new_wod: Logs a new WOD entry into the DataFrame and updates the CSV file.
        log_wod: Adds a new session record for an existing WOD.
        wod_exists: Checks if a WOD already exists in the DataFrame.
        get_wod_details: Retrieves details for a specific WOD.
    """

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
        self.df_wods = self.df_wods.append(new_data, ignore_index=True)
        self.df_wods.to_csv(self.csv_path, index=False)

    def wod_exists(self, wod_name):
        return wod_name in self.df_wods['WOD Name'].values

    def get_wod_details(self, wod_name):
        if self.wod_exists(wod_name):
            return self.df_wods[self.df_wods['WOD Name'] == wod_name].iloc[0].to_dict()
        return {}

    def log_wod(self, wod_name, wod_description, wod_date, wod_time, wod_category, wod_details):
        if not self.wod_exists(wod_name):
            return "WOD does not exist. Please add it first."
        new_data = {
            'WOD Name': wod_name,
            'Description': wod_description,
            'Date': wod_date,
            'Time': wod_time,
            'Category': wod_category,
            'Details': wod_details
        }
        self.df_wods = self.df_wods.append(new_data, ignore_index=True)
        self.df_wods.to_csv(self.csv_path, index=False)
        return "New WOD session logged successfully."
