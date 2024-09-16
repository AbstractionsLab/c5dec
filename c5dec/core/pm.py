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

log.setLevel(common.logging.INFO)

logHandler = common.logging.FileHandler(c5settings.PM_LOG_FILE, mode='a')
formatter = common.logging.Formatter("%(asctime)s - %(levelname)s - %(funcName)s() : %(message)s", "%Y-%m-%d %H:%M:%S")
logHandler.setFormatter(formatter)
log.addHandler(logHandler)

# TO-REDESIGN: change your data and not the code: eliminate all hard-coded schema details from TimeReportAssistant and link to YAML schema file
# TO-DO: refactor the consolidation and OpenProject conversion code to use the c5dec_params YAML file like the cost rep function as per redesign above

class TimeReportAssistant:
    """The model of the time report assistant.
    
    This is the model part of the MVC strcuture.
    """
    def __init__(self):
        """Set up the key attributes needed for time report assistance.
        """
        self.input_file_path = ""
        self.input_file_name = None
        self.tsh_folder_name = "tsh-to-merge"
        self.tsh_folder_path = "."
        self.apply_filters = False
        self.from_date = None
        self.to_date = None
        self.filter_field = ""
        self.filter_field_value = "" 
        self.df = None
        self.consolidated_tsh_df = None
        self.param_df_dict = None

    def set_tsh_folder_path(self, path):
        self.tsh_folder_path = path

    def set_tsh_folder_name(self, tsh_folder_name):
        if tsh_folder_name is None:
            self.tsh_folder_name = "tsh-to-merge"
        else:
            self.tsh_folder_name = tsh_folder_name

    def set_timerep_parameters(self, source_folder, apply_filters=False, from_date=None, to_date=None,
                               filter_field="", filter_field_value=""):
        # self.tsh_folder_path = source_folder
        self.tsh_folder_name = source_folder
        self.apply_filters = apply_filters
        self.from_date = from_date
        self.to_date = to_date
        self.filter_field = filter_field
        self.filter_field_value = filter_field_value

    def get_timerep_fields(self):
        return self.read_tshparams_config_into_dict().get("ALab-TSH-columns")

    def consolidate_timesheets(self):
        # folder = self.tsh_folder_path
        folder = os.path.join(c5settings.INPUT_FOLDER_NAME, self.tsh_folder_name)
        folder_obj = pathlib.Path(folder)

        df = None
        columns = self.read_tshparams_config_into_dict().get("ALab-TSH-columns")
        for index, item in enumerate(folder_obj.iterdir()):
            if not item.is_dir():
                log.info("Processing {}".format(item))
                if not (pathlib.Path(item).suffix in ['.xlsx', '.xls']):
                    log.info("Skipping non xls/xlsx file: {}".format(item))
                    continue
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
        # df = pd.read_excel(self.input_file_path, sheet_name=1, skiprows=[0]).dropna()
        df = pd.read_excel(os.path.join(c5settings.INPUT_FOLDER_NAME, self.input_file_name), sheet_name=1, skiprows=[0]).dropna()

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
        log.info("Saving C5-DEC time sheet to {}".format(file_path))
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
    
    def compute_cost_report(self):
        # Read RMT parameter tables
        tables_list = c5settings.c5params_dictionary.get('pm').get('cost').get('sheet-tables')

        tables_input_file_path = c5settings.RMT_PARAMS_FILE_PATH
        self.param_df_dict = dict()
        for table in tables_list:
            try:
                df = pd.read_excel(tables_input_file_path, sheet_name=table)
                self.param_df_dict[table] = df
            except Exception as e:
                print(e)

        # Read TSH
        INPUT_FILE_NAME = self.input_file_name
        try:
            timesheet_sheet_name = c5settings.c5params_dictionary.get('pm').get('tsh').get('sheet-name')
            tsh_df = pd.read_excel(os.path.join(c5settings.INPUT_FOLDER_NAME, INPUT_FILE_NAME), sheet_name=timesheet_sheet_name)
        except Exception as e:
            print(e)

        # Build cost df
        # cost_df = self.normalize_tsh(tsh_df.copy())
        cost_df = tsh_df.copy()
        verif_df = tsh_df.copy()

        daily_rate_col_name = c5settings.c5params_dictionary.get('pm').get('cost').get('daily-rate-col-name')
        cost_df[daily_rate_col_name] = len(tsh_df.index)*[0]
        
        cost_col_name = c5settings.c5params_dictionary.get('pm').get('cost').get('cost-col-name')
        cost_df[cost_col_name] = len(tsh_df.index)*[0]

        self_fund_cost_col_name = c5settings.c5params_dictionary.get('pm').get('cost').get('self-fund-cost-col-name')
        cost_df[self_fund_cost_col_name] = len(tsh_df.index)*[0]

        cofund_contrib_col_name = c5settings.c5params_dictionary.get('pm').get('cost').get('cofund-contribution-col-name')
        cost_df[cofund_contrib_col_name] = len(tsh_df.index)*[0]

        compute_verif_col_name = c5settings.c5params_dictionary.get('pm').get('cost').get('computation-verification-col-name')
        cost_df[compute_verif_col_name] = len(tsh_df.index)*[0]

        for idx, row in cost_df.iterrows():
            daily_rate, cofund_contrib, self_fund_cost, compute_verif_dict = self.compute_daily_rate_for_tsh_row(row)
            cost_df.loc[idx, daily_rate_col_name] = daily_rate

            compute_verif_col_name = c5settings.c5params_dictionary.get('pm').get('cost').get('computation-verification-col-name')
            compute_verif_cell_value = ""
            for k, v in compute_verif_dict.items():
                verif_df.loc[idx, k] = v
                compute_verif_cell_value += "".join([str(k), ": ", str(v)])
            
            cost_df.loc[idx, compute_verif_col_name] = compute_verif_cell_value

            if isinstance(daily_rate, float) or isinstance(daily_rate, int):
                days_spent_col_name = c5settings.c5params_dictionary.get('pm').get('tsh').get('days-spent') 
                cost = daily_rate * row[days_spent_col_name]
                cost_df.loc[idx, cost_col_name] = cost
                cost_df.loc[idx, self_fund_cost_col_name] = self_fund_cost * row[days_spent_col_name]
                cost_df.loc[idx, cofund_contrib_col_name] = cofund_contrib * row[days_spent_col_name]
        
        current_time = time.strftime("%Y%m%d-%H%M%S")
        file_path = "{0}/cost-report-{1}.xlsx".format(os.getcwd(), current_time)
        
        log.info("Saving cost report to xlsx file: {0}".format(file_path))

        writer = pd.ExcelWriter(file_path)
        cost_df.to_excel(writer, sheet_name="CostReport", index=False)
        verif_df.to_excel(writer, sheet_name="VerificationSheet", index=False)
        writer.close()

    def compute_daily_rate_for_tsh_row(self, row):
        type = row[c5settings.c5params_dictionary.get('pm').get('tsh').get('type')]
        dom = row[c5settings.c5params_dictionary.get('pm').get('tsh').get('domain')]
        wp = row[c5settings.c5params_dictionary.get('pm').get('tsh').get('wp')]
        acr = row[c5settings.c5params_dictionary.get('pm').get('tsh').get('id')]
        month = row[c5settings.c5params_dictionary.get('pm').get('tsh').get('month')]
        year = row[c5settings.c5params_dictionary.get('pm').get('tsh').get('year')]

        soc_sec_col = c5settings.c5params_dictionary.get('pm').get('cost').get('social-security')
        mg_overhead_col = c5settings.c5params_dictionary.get('pm').get('cost').get('mg-overhead') 
        bi_overhead_col = c5settings.c5params_dictionary.get('pm').get('cost').get('bi-overhead')
        effective_days_col = c5settings.c5params_dictionary.get('pm').get('cost').get('effective-days')
        fixed_rate_used_col = c5settings.c5params_dictionary.get('pm').get('cost').get('is-fixed-rate-used')
        cofunding_rate_col = c5settings.c5params_dictionary.get('pm').get('cost').get('cofunding-rate-col-name')
        
        act_rates = self.get_activity_tuple_rates(type, dom, wp)
        salary = self.get_salary(acr, month, year)
        
        if act_rates.empty:
            log.info("Activity rate data frame empty for {}, {}, {}".format(type, dom, wp))
            return "No activity info found (Type, Domain and WP mapping)", "None", "None", {"Verif: ": "See ActivityCostParams sheet in rmt-params"}
        
        if salary.empty:
            log.info("Salary data frame empty for {}, {}, {}".format(acr, year, month))
            return "No salary info found (ACR, Year and Month)", "None", "None", {"Verif: ": "See StaffParams sheet in rmt-params"}

        if act_rates[fixed_rate_used_col].values[0] == 1:
            cofunding_rate = act_rates[cofunding_rate_col].values[0]
            fixed_daily_rate = self.get_fixed_daily_rate(acr, month, year, type, dom)
            return fixed_daily_rate, fixed_daily_rate*cofunding_rate, fixed_daily_rate*(1-cofunding_rate), {"Verif: ": "See fixed rate table in FixedRates sheet"}
        else:
            social_sec_contrib = act_rates[soc_sec_col].values[0]
            mg_overhead_rate = act_rates[mg_overhead_col].values[0]
            bi_overhead_rate = act_rates[bi_overhead_col].values[0]
            effective_days = act_rates[effective_days_col].values[0]
            cofunding_rate = act_rates[cofunding_rate_col].values[0]

            gross_salary_col_name = c5settings.c5params_dictionary.get('pm').get('cost').get('gross-salary-col-name')
            compute_verif_dict = {gross_salary_col_name: str(salary.values[0]), 
                                       cofunding_rate_col: str(cofunding_rate), 
                                       soc_sec_col: str(social_sec_contrib),
                                       mg_overhead_col: str(mg_overhead_rate),
                                       bi_overhead_col: str(bi_overhead_rate),
                                       effective_days_col: str(effective_days)}

            daily_rate = salary.values[0] * (1+social_sec_contrib) * (1+mg_overhead_rate) * (1+bi_overhead_rate) / effective_days
            return daily_rate, daily_rate*cofunding_rate, daily_rate*(1-cofunding_rate), compute_verif_dict
    
    def get_fixed_daily_rate(self, acr, month, year, type, domain):
        # Read staff parameters table into a data frame
        staff_params_sheet_name = c5settings.c5params_dictionary.get('pm').get('cost').get('sheet-tables')[0]
        df = self.param_df_dict[staff_params_sheet_name]

        acr_col_name = c5settings.c5params_dictionary.get('pm').get('tsh').get('id')
        month_col_name = c5settings.c5params_dictionary.get('pm').get('tsh').get('month')
        year_col_name = c5settings.c5params_dictionary.get('pm').get('tsh').get('year')

        # Get staff parameter row for person acronym, year, and month
        row = df.loc[(df[acr_col_name] == acr) & (df[year_col_name] == year) & (df[month_col_name] == month)]

        # Get staff member qualification or staff category type
        # Build type-domain staff category column header
        staff_type_col_name = c5settings.c5params_dictionary.get('pm').get('cost').get('staff-type-col-name')

        type_domain_staff_category_category_col_name = "".join([type, "-", domain, "-", staff_type_col_name])
        acr_staff_type = row[type_domain_staff_category_category_col_name].values[0]
        
        # Read fixed rates parameters table into a data frame
        fixed_rates_params_sheet_name = c5settings.c5params_dictionary.get('pm').get('cost').get('sheet-tables')[2]
        fixed_rates_df = self.param_df_dict[fixed_rates_params_sheet_name]
        
        daily_rate_col_name = c5settings.c5params_dictionary.get('pm').get('cost').get('daily-rate-col-name')

        daily_rate_row = fixed_rates_df.loc[fixed_rates_df[staff_type_col_name] == acr_staff_type]
        daily_rate = daily_rate_row[daily_rate_col_name].values[0]

        return float(daily_rate)

    def get_salary(self, acr, month, year):
        # Read staff parameters table into a data frame
        staff_params_sheet_name = c5settings.c5params_dictionary.get('pm').get('cost').get('sheet-tables')[0]
        df = self.param_df_dict[staff_params_sheet_name]
        
        acr_col_name = c5settings.c5params_dictionary.get('pm').get('tsh').get('id')
        month_col_name = c5settings.c5params_dictionary.get('pm').get('tsh').get('month')
        year_col_name = c5settings.c5params_dictionary.get('pm').get('tsh').get('year')

        salary_row = df.loc[(df[acr_col_name] == acr) & (df[year_col_name] == year) & (df[month_col_name] == month)]

        gross_salary_col_name = c5settings.c5params_dictionary.get('pm').get('cost').get('gross-salary-col-name')
        return salary_row[gross_salary_col_name]
    
    def get_activity_tuple_rates(self, type, domain, wp):
        # Read activity cost parameters table into a data frame
        activity_cost_params_sheet_name = c5settings.c5params_dictionary.get('pm').get('cost').get('sheet-tables')[1]
        df = self.param_df_dict[activity_cost_params_sheet_name]

        type_col_name = c5settings.c5params_dictionary.get('pm').get('tsh').get('type')
        dom_col_name = c5settings.c5params_dictionary.get('pm').get('tsh').get('domain')
        wp_col_name = c5settings.c5params_dictionary.get('pm').get('tsh').get('wp')
        activity_rates = df.loc[(df[type_col_name].str.fullmatch(type, case=False)) & (df[dom_col_name].str.fullmatch(domain, case=False)) & (df[wp_col_name].str.fullmatch(str(wp), case=False))]
        return activity_rates
    
    def normalize_tsh(self, tsh):
        # dom_col_name = c5settings.c5params_dictionary.get('pm').get('tsh').get('domain')
        # tsh[dom_col_name] = tsh[dom_col_name].apply(lambda x: x.upper())
        return tsh