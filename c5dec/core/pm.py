from datetime import datetime, timedelta, date
import time
import json
import numpy as np
import pandas as pd
import os
import pathlib
import re
import warnings
import c5dec.settings as c5settings
import c5dec.common as common
log = common.logger(__name__)
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

class TimeReportAssistant:
    """The model of the time report assistant.
    
    This is the model part of the MVC strcuture.
    """
    def __init__(self):
        """Set up the key attributes needed for time report assistance.
        """
        self.input_file_path = ""
        self.tsh_folder_path = "."
        self.apply_filters = False
        self.from_date = None
        self.to_date = None
        self.filter_field = ""
        self.filter_field_value = "" 
        self.df = None
        self.consolidated_tsh_df = None

    def set_tsh_folder_path(self, path):
        self.tsh_folder_path = path

    def set_timerep_parameters(self, source_folder, apply_filters=False, from_date=None, to_date=None,
                               filter_field="", filter_field_value=""):
        self.tsh_folder_path = source_folder
        self.apply_filters = apply_filters
        self.from_date = from_date
        self.to_date = to_date
        self.filter_field = filter_field
        self.filter_field_value = filter_field_value

    def get_timerep_fields(self):
        return self.read_tshparams_config_into_dict().get("ALab-TSH-columns")

    def consolidate_timesheets(self):
        folder = self.tsh_folder_path
        folder_obj = pathlib.Path(folder)

        df = None
        columns = self.read_tshparams_config_into_dict().get("ALab-TSH-columns")
        for index, item in enumerate(folder_obj.iterdir()):
            if not item.is_dir():
                if index == 0:
                    df = pd.read_excel(item, sheet_name='Timesheet')
                    df = df[columns]
                else:
                    df_new = pd.read_excel(item, sheet_name='Timesheet')
                    df_new = df_new[columns]
                    df = pd.concat([df, df_new], ignore_index=True)

        if self.apply_filters == True:
            filtered_df = None

            df['Date'] = pd.to_numeric(df['Date'], errors='coerce')
            df['Date'] = df['Date'].fillna(0).astype(int)
            df = df.dropna(subset=['Date'])
            
            df['MM'] = pd.to_numeric(df['MM'], errors='coerce')
            df['MM'] = df['MM'].fillna(0).astype(int)
            df = df.dropna(subset=['MM'])

            if self.from_date != None and self.to_date != None:
                filtered_df = df.query("MM >= {} and MM <= {}".format(self.from_date.month, self.to_date.month))

            if self.filter_field != "" and self.filter_field_value != "":
                filtered_df = filtered_df.loc[filtered_df[self.filter_field] == self.filter_field_value]

            df = filtered_df

        self.consolidated_tsh_df = df

        self.clean_consolidated_dataframe()
        self.save_consolidated_tsh_df_to_excel()

    def make_date_field(self, row):
        try:
            date_object = date(year=row["Year"], month=row["MM"], day=row["Date"])
            return date_object
        except Exception as e:
            log.info("invalid date at row {}...".format(row))
            return False

    def clean_consolidated_dataframe(self):
        df = self.consolidated_tsh_df
 
        df = df.dropna(axis=0, how='all')

        self.consolidated_tsh_df = df

    def convert_openproject_time_report_to_IAL_format(self):
        df = pd.read_excel(self.input_file_path, sheet_name=1, skiprows=[0]).dropna()

        self.add_missing_columns(df)
        # Parameters file containing WP to type and domain mappings
        openproject_params_df = self.read_csv_to_df(c5settings.OPENPROJECT_PARAMS_CSV_FILE_PATH)

        # Staff name acronyms
        staff_acr_dict = self.get_staff_acronyms_dictionary()
        df.replace({"User": staff_acr_dict}, inplace=True)
        
        # Apply mappings to populate newly added columns
        self.replace_key_with_value_in_df_column(df, "Type", openproject_params_df.WP, openproject_params_df.Type)
        self.replace_key_with_value_in_df_column(df, "Domain/Project name", openproject_params_df.WP, openproject_params_df.Domain)

        # Convert the OpenProject Date (Spent) value to day, month, year and weekday
        df["Date"] = df["Date"].apply(lambda x: str(x).split('-')[2])
        df["MM"] = df["MM"].apply(lambda x: str(x).split('-')[1])
        df["YYYY"] = df["YYYY"].apply(lambda x: str(x).split('-')[0])
        df["Day"] = df["Day"].apply(lambda x: pd.Timestamp(x).day_name())
        
        # Extract start time from the Comment field; compute end time based on duration; populate both columns
        df = self.extract_time_interval(df, "Start", "End", "Units")

        # Rename columns according to ALab TSH template
        df.rename(columns={"User": "ACR", "Activity": "Task", "Project": "Cust/WP", "Units": "Hours", "Work package": "Description"}, inplace=True)

        # Adapt the column ordering according to ALab TSH template
        new_col_order = ['ACR', 'Date', 'MM', 'YYYY', 'Day', 'Type', 'Domain/Project name', 'Cust/WP', 'Task', 'Location', 'Start', 'End', 'Hours', 'Days', 'Description']
        df = df[new_col_order]

        self.df = df

        self.save_processed_timerep_df_to_excel()

        return df

    def read_csv_to_df(self, csv_path) -> pd.DataFrame:
        return pd.read_csv(csv_path)

    def read_tshparams_config_into_dict(self):
        with open(c5settings.TSHFORMAT_JSON_FILE_PATH) as tshformat_json_file:
            tshformat_json_file_content = tshformat_json_file.read()

        parsed_tshformat = json.loads(tshformat_json_file_content)
        return parsed_tshformat
    
    def save_consolidated_tsh_df_to_excel(self) -> None:
        current_time = time.strftime("%Y%m%d-%H%M%S")
        file_path = "{0}/consolidated-TSH-{1}.xlsx".format(os.getcwd(), current_time)
        self.consolidated_tsh_df.to_excel(file_path)
    
    def save_processed_timerep_df_to_excel(self) -> None:
        current_time = time.strftime("%Y%m%d-%H%M%S")
        file_path = "{0}/output-{1}.xlsx".format(os.getcwd(), current_time)
        self.df.to_excel(file_path)

    def get_staff_acronyms_dictionary(self):
        """Get all acronyms that are stored in a json file.
        
        :param file: the file that stores acronyms (.json)
        :type file: str
        
        :return: a list that contains all acronyms in the file
        :rtype: list
        """
        staff_acr_file_path = c5settings.PERSON_ACRONYMS_FILE_PATH

        # read file
        with open(staff_acr_file_path, 'r') as file:
            data = file.read()

        # parse file
        acr_dict = json.loads(data)
        
        return acr_dict
    
    def add_missing_columns(self, df):
        df["Date"] = df["Date (Spent)"]
        df["MM"] = df["Date (Spent)"]
        df["YYYY"] = df["Date (Spent)"]
        df["Day"] = df["Date (Spent)"]
        df["Type"] = df["Project"]
        df["Domain/Project name"] = df["Project"]
        df["Location"] = df["User"]
        df["Start"] = df["Comment"]
        df["End"] = df["Comment"]
        df["Days"] = df["Units"]/8.0
    
    def replace_key_with_value_in_df_column(self, dataframe, df_col_name, key_list, value_list):
            keyvalue_dict = dict(zip(key_list, value_list))
            dataframe.replace({df_col_name: keyvalue_dict}, inplace=True)

    def extract_time_interval(self, df, start_col_name, end_col_name, duration_col_name):
        df_copy = df.copy()
        for index, row in df.iterrows():
            start_cell = row[start_col_name]
            duration = row[duration_col_name]
            result = re.search(r".*{(\d+:\d+)}.*", start_cell)
            if not result == None:
              df_copy.at[index, start_col_name] = result.group(1)
              df_copy.at[index, end_col_name] = (datetime.strptime(str(result.group(1)), "%H:%M") + timedelta(minutes=duration*60.0)).strftime('%H:%M')
        return df_copy