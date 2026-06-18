import pandas as pd
import numpy as np
import re

#  "empty_cells": {"first_name": [1, 5], "phone": [12]}
def check_empty_cells(df: pd.DataFrame):
    df.replace("", np.nan, inplace=True)
    empty_cells = {}
    if df.isna().any().any():
        row_ind, col_ind = np.where(df.isna())
        for row, col_num in zip(row_ind, col_ind):
            col_name = df.columns[col_num]
            if col_name not in empty_cells:
                empty_cells[col_name] = []
            empty_cells[col_name].append(row)
        return empty_cells
    else:
        return {}


# "invalid_emails": [3, 7, 42],  
def check_emails(df: pd.DataFrame):
    invalid_emails = []
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    for index, email in df["Email"].items():
        if pd.isna(email):
            continue
        if not re.match(pattern, email):
            invalid_emails.append(index)
    if not invalid_emails:
        return []
    return invalid_emails
    
# "invalid_phones": [2, 9, 15],
def check_phone_numbers(df: pd.DataFrame):
    invalid_phones = []
    for index, phone in df["Phone"].items():
        if pd.isna(phone):
            continue
        numbers_only = re.sub(r'[^\d]', '', phone)
        if len(numbers_only) != 10 and len(numbers_only) != 11:
            invalid_phones.append(index)
    if not invalid_phones:
        return []
    return invalid_phones
    
def check_dates(df: pd.DataFrame):
    invalid_dates = []
    # current_year = pd.Timestamp.now().year
    for index, dob in df["Date of birth"].items():
        parsed_date = pd.to_datetime(dob, format="%Y-%m-%d", errors='coerce')
        if pd.isna(parsed_date):
            invalid_dates.append(index)
            continue
        if pd.Timestamp.now() < parsed_date:
            invalid_dates.append(index)
    return invalid_dates

def check_sex_values(df: pd.DataFrame):
    invalid_sex = []
    allowed_sex = ["male","female"]
    for index, sex in df["Sex"].items():
        if pd.isna(sex):
            continue
        if str(sex).strip().lower() not in allowed_sex:
            invalid_sex.append(index)
    return invalid_sex

def check_duplicates(df: pd.DataFrame):
    duplicates = set()
    # num_rows = len(df) 
    important_col = ["User Id", "Phone", "Email"]
    exact_duplicates = df.index[df.duplicated()].tolist()
    duplicates.update(exact_duplicates)
    duplicates.update(df.index[df.duplicated(subset="User Id")].tolist())
    duplicates.update(df.index[df.duplicated(subset=["Phone", "Email"])].tolist())
    # for i in important_col:
    #     if i in df.columns:
    #         duplicates.update(df.index[df.duplicated(subset=i)].tolist())
    #     continue
    return list(duplicates)

def validate(df: pd.DataFrame):
    report = {}
    report["empty_cells"] = check_empty_cells(df)
    report["invalid_emails"] = check_emails(df)
    report["invalid_phones"] = check_phone_numbers(df)
    report["duplicates"] = check_duplicates(df)
    report["invalid_sex"] = check_sex_values(df)
    report["invalid_dates"] = check_dates(df)
    # report["invalid_jobs"] = check_jobs(df)

    return report


