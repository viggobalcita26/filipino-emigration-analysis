import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os

PATH = os.getenv("SYSTEM_DATA_PATH", "defautl/fallback/path")

def extract(file, sheet_name=0, skip_rows=2):
    try:
        raw_data = pd.read_excel(f"{PATH}{file}", sheet_name=sheet_name, skiprows=skip_rows)
        return raw_data
    
    except FileNotFoundError:
        print("File was not found. Check file path")


def clean(df_raw):
    try:
        # clean the headers and drop unnamed columns
        df_raw.columns = df_raw.columns.astype(str).str.strip()
        df_raw = df_raw.loc[:, ~df_raw.columns.str.contains("unnamed", case=False, na=False)]
                            
        # drop NaN rows in the first column
        first_col = df_raw.columns[0]
        df_raw[first_col] = df_raw[first_col].astype(str).str.strip().replace(["", "nan", "NaN"], np.nan)
        df_clean = df_raw.dropna(how="all", subset=[first_col])
       

        # drop unncessary rows in first column
        is_summary_row = df_clean[first_col].astype(str).str.contains(
            "Total|Source|Sub-Total|Annual Average|T O T A L", 
            case=False, 
            na=False
        )
        df_clean = df_clean[~is_summary_row]

        # fill NaN columns with 0 
        df_clean = df_clean.fillna(0)

        # make all numerical values into int
        years_in_df = [col for col in df_clean.columns if col in map(str, range(1981, 2021))]
        for col in years_in_df:
            df_clean[col] = df_clean[col].astype(str).str.strip().replace(["", "nan", "NaN"], np.nan)
            df_clean[col] = df_clean[col].fillna(0)
        df_clean[years_in_df] = df_clean[years_in_df].astype(float).astype(int)
        return df_clean
    

    except Exception as e:
        print(f"An error occured during transformation: {e}")

def load(df, file_name):
    try:
        df.to_csv(f"{PATH}{file_name}", index=False)
        print(f"downloaded csv file {file_name}")
    except Exception as e:
        print(f"Unable to download file: {e}")
