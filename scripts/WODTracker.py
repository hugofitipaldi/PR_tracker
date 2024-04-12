import pandas as pd

class WODTracker:
    """
    A class to track workout of the day (WOD) records using a CSV file as a data store.

    Attributes:
        csv_path (str): The file path to the CSV file where WOD records are stored.
        df_wods (DataFrame): A pandas DataFrame containing the WOD records.

    Methods:
        log_new_wod(wod_name, wod_description, wod_date, wod_time, wod_category, wod_details):
            Logs a new WOD entry into the DataFrame and updates the CSV file.
    """

    def __init__(self, csv_path='../data/benchmark_wods.csv'):
        """
        Initializes the WODTracker with a specified path to a CSV file.

        If the CSV file exists at the given path, it loads the existing data into the DataFrame.
        If the file does not exist, it creates a new CSV file with the required columns.

        Parameters:
            csv_path (str): The path to the CSV file where WOD records are stored. Defaults to '../data/benchmark_wods.csv'.
        """
        self.csv_path = csv_path
        try:
            self.df_wods = pd.read_csv(csv_path)
        except FileNotFoundError:
            columns = ['WOD Name', 'Description', 'Date', 'Time', 'Category', 'Details']
            self.df_wods = pd.DataFrame(columns=columns)
            self.df_wods.to_csv(csv_path, index=False)

    def log_new_wod(self, wod_name, wod_description, wod_date, wod_time, wod_category, wod_details):
        """
        Logs a new WOD record in the DataFrame and updates the CSV file with the new data.

        Parameters:
            wod_name (str): The name of the WOD.
            wod_description (str): A description of the WOD.
            wod_date (str): The date when the WOD was performed.
            wod_time (str): The time taken to complete the WOD.
            wod_category (str): The category of the WOD (e.g., strength, conditioning).
            wod_details (str): Additional details about the WOD (e.g., weights used, rounds completed).

        Returns:
            None
        """
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
