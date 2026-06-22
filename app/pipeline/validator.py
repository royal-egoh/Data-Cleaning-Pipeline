import pandas as pd
import numpy as np
import re

#  "empty_cells": {"first_name": [1, 5], "phone": [12]}


def check_empty_cells(df: pd.DataFrame):
    df.replace("", np.nan, inplace=True)
    # empty_cells = {}
    if not df.isna().any().any():
        return {}
    else:
        return {col: df.index[df[col].isna()].tolist() for col in df.columns if df[col].isna().any().any()}


# "invalid_emails": [3, 7, 42],
def check_emails(df: pd.DataFrame):
    invalid_emails = []
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    emails = df["Email"].str.match(pattern, na=True)
    return df.index[~emails].tolist()
    
# "invalid_phones": [2, 9, 15],


def check_phone_numbers(df: pd.DataFrame):
    invalid_phones = []
    invalid_phones.extend([index for index, phone in df["Phone"].items() if len(re.sub(r'[^\d]', '', str(phone))) not in [10, 11]])
    return invalid_phones


def check_dates(df: pd.DataFrame):
    invalid_dates = []
    parsed_date = pd.to_datetime(
        df["Date of birth"], format="%Y-%m-%d", errors='coerce')
    invalid_dates.extend(df.index[parsed_date.isna()].tolist())
    now = pd.Timestamp.now()
    invalid_dates.extend(df.index[parsed_date > now].tolist())
    return invalid_dates


def check_sex_values(df: pd.DataFrame):
    invalid_sex = []
    allowed_sex = ["male", "female", "f", "m"]
    clean_sx = df["Sex"].astype(str).str.strip().str.lower()
    invalid = ~clean_sx.isin(allowed_sex)
    invalid_sex.extend(df.index[invalid].tolist())
    return invalid_sex

def check_duplicates(df: pd.DataFrame):
    duplicates = set()
    # num_rows = len(df)
    important_col = ["User Id", "Phone", "Email"]
    exact_duplicates = df.index[df.duplicated()].tolist()
    duplicates.update(exact_duplicates)
    duplicates.update(df.index[df.duplicated(subset="User Id")].tolist())
    duplicates.update(df.index[df.duplicated(
        subset=["Phone", "Email"])].tolist())
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
