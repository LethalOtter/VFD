import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def load_csv(file_path):
    try:
        print(f"Loading file: {file_path}")
        with open(file_path, 'r') as f:
            lines = f.readlines()
        header_info = {}
        for line in lines[:9]:
            if ',' in line:
                key, value = line.strip().split(',', 1)
                header_info[key] = value
        print(f"Header info: {header_info}")
        if '\n' in lines:
            data_start_index = lines.index('\n') + 1
        else:
            raise ValueError("No blank line found to separate header and data sections")
        print(f"Data starts at line: {data_start_index}")
        data_df = pd.read_csv(file_path, skiprows=data_start_index)
        for key, value in header_info.items():
            data_df[key] = value
        print("File loaded successfully.")
        return data_df
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

def search_by_aoa(df, aoa_min, aoa_max):
    try:
        print(f"Searching for aoa in range: {aoa_min} to {aoa_max}")
        aoa_df = df[(df['Alpha'] >= aoa_min) & (df['Alpha'] <= aoa_max)]
        print(f"Search by aoa completed. Found {len(aoa_df)} records.")
        return aoa_df
    except Exception as e:
        print(f"Error searching by aoa: {e}")
        return None

def search_by_cd(df, cd_min, cd_max):
    try:
        print(f"Searching for Cd in range: {cd_min} to {cd_max}")
        cd_df = df[(df['Cd'] >= cd_min) & (df['Cd'] <= cd_max)]
        print(f"Search by Cd completed. Found {len(cd_df)} records.")
        return cd_df
    except Exception as e:
        print(f"Error searching by Cd: {e}")
        return None

def search_by_cl(df, cl_min, cl_max):
    try:
        print(f"Searching for Cl in range: {cl_min} to {cl_max}")
        cl_df = df[(df['Cl'] >= cl_min) & (df['Cl'] <= cl_max)]
        print(f"Search by Cl completed. Found {len(cl_df)} records.")
        return cl_df
    except Exception as e:
        print(f"Error searching by Cl: {e}")
        return None

def search_by_cdp(df, cdp_min, cdp_max):
    try:
        print(f"Searching for Cdp in range: {cdp_min} to {cdp_max}")
        cdp_df = df[(df['Cdp'] >= cdp_min) & (df['Cdp'] <= cdp_max)]
        print(f"Search by Cdp completed. Found {len(cdp_df)} records.")
        return cdp_df
    except Exception as e:
        print(f"Error searching by Cdp: {e}")
        return None

def search_by_cm(df, cm_min, cm_max):
    try:
        print(f"Searching for Cm in range: {cm_min} to {cm_max}")
        cm_df = df[(df['Cm'] >= cm_min) & (df['Cm'] <= cm_max)]
        print(f"Search by Cm completed. Found {len(cm_df)} records.")
        return cm_df
    except Exception as e:
        print(f"Error searching by Cm: {e}")
        return None

def search_by_top_xtr(df, top_xtr_min, top_xtr_max):
    try:
        print(f"Searching for Top_Xtr in range: {top_xtr_min} to {top_xtr_max}")
        top_xtr_df = df[(df['Top_Xtr'] >= top_xtr_min) & (df['Top_Xtr'] <= top_xtr_max)]
        print(f"Search by Top_Xtr completed. Found {len(top_xtr_df)} records.")
        return top_xtr_df
    except Exception as e:
        print(f"Error searching by Top_Xtr: {e}")
        return None

def search_by_bot_xtr(df, bot_xtr_min, bot_xtr_max):
    try:
        print(f"Searching for Bot_Xtr in range: {bot_xtr_min} to {bot_xtr_max}")
        bot_xtr_df = df[(df['Bot_Xtr'] >= bot_xtr_min) & (df['Bot_Xtr'] <= bot_xtr_max)]
        print(f"Search by Bot_Xtr completed. Found {len(bot_xtr_df)} records.")
        return bot_xtr_df
    except Exception as e:
        print(f"Error searching by Bot_Xtr: {e}")
        return None

def get_range_input(param_name):
    min_val = input(f"Enter minimum value for {param_name} (or 'NA' to skip): ")
    try:
        min_val = float(min_val)
    except ValueError:
        return None, None
    max_val = input(f"Enter maximum value for {param_name} (or 'NA' to skip): ")
    try:
        return min_val, float(max_val)
    except ValueError:
        return None, None

def main():
    Tk().withdraw()
    filepath = askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not filepath:
        print("No file selected.")
        return
    print(f"Selected file: {filepath}")
    df = load_csv(filepath)
    if df is not None:
        aoa_min, aoa_max = get_range_input('Alpha')
        if aoa_min is not None and aoa_max is not None:
            aoa_df = search_by_aoa(df, aoa_min, aoa_max)
            print(aoa_df)
        
        cd_min, cd_max = get_range_input('Cd')
        if cd_min is not None and cd_max is not None:
            cd_df = search_by_cd(df, cd_min, cd_max)
            print(cd_df)
        
        cl_min, cl_max = get_range_input('Cl')
        if cl_min is not None and cl_max is not None:
            cl_df = search_by_cl(df, cl_min, cl_max)
            print(cl_df)
        
        cdp_min, cdp_max = get_range_input('Cdp')
        if cdp_min is not None and cdp_max is not None:
            cdp_df = search_by_cdp(df, cdp_min, cdp_max)
            print(cdp_df)
        
        cm_min, cm_max = get_range_input('Cm')
        if cm_min is not None and cm_max is not None:
            cm_df = search_by_cm(df, cm_min, cm_max)
            print(cm_df)
        
        top_xtr_min, top_xtr_max = get_range_input('Top_Xtr')
        if top_xtr_min is not None and top_xtr_max is not None:
            top_xtr_df = search_by_top_xtr(df, top_xtr_min, top_xtr_max)
            print(top_xtr_df)
        
        bot_xtr_min, bot_xtr_max = get_range_input('Bot_Xtr')
        if bot_xtr_min is not None and bot_xtr_max is not None:
            bot_xtr_df = search_by_bot_xtr(df, bot_xtr_min, bot_xtr_max)
            print(bot_xtr_df)
    else:
        print("Dataframe is None, cannot proceed with search.")

if __name__ == "__main__":
    main()