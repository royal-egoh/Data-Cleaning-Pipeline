import pandas as pd
import phonenumbers
import re
from joblib import Parallel, delayed
import numpy as np


# {
#     "invalid_emails": [3, 7, 42],      ?
#     "empty_cells": {"first_name": [1, 5], "phone": [12]}
#     "invalid_phones": [2, 9, 15],     ?
#     "invalid_dates": [6, 11],         ?
#     "invalid_sex": [4, 8],            ?
#     "duplicates": [13, 14]
# }

def drop_invaldid_rows(df: pd.DataFrame, report: dict):
    invalid_emails = set(report.get("invalid_emails", []))
    invalid_phones = set(report.get("invalid_phones", []))
    empty_cells = report.get("empty_cells", {})
    
    empty_phones = set(empty_cells.get("Phone", []))
    empty_emails = set(empty_cells.get("Email", []))
    
    all_bad_phones = invalid_phones.union(empty_phones)
    all_bad_emails = invalid_emails.union(empty_emails)
    
    invalid_intersection = all_bad_emails.intersection(all_bad_phones)
    empty_user_id = set(empty_cells.get("User Id", []))
    
    row_to_drop = invalid_intersection.union(empty_user_id)
    
    df = df.drop(index=[item for item in row_to_drop if item in df.index])
    return df

def fill_nulls(df: pd.DataFrame, report: dict):
    invalid_sex = set(report.get("invalid_sex", []))
    invalid_dates = set(report.get("invalid_dates", []))
    empty_cells = report.get("empty_cells", {})
    empty_cells["Sex"] = list(invalid_sex)
    empty_cells["Date of birth"] = list(invalid_dates)
    
    columns_to_fill = [
        "First Name", 
        "Last Name",
        "Sex",
        "Email", 
        "Phone", 
        "Date of birth", 
        "Job Title"
    ]
    for col in columns_to_fill:
        empty = set(empty_cells.get(col, []))
        if empty:
            df.loc[[i for i in empty if i in df.index], col] = "Null"
    
    return df

def standardise_phone(df: pd.DataFrame):
    def parse_single_phone(phone):
        if pd.isna(phone) or str(phone).strip() == "Null":
            return "Null"
        try:
            phone_str = str(phone).strip()
            if phone_str.startswith("001"):
                phone_str = "+" + phone_str[2:].lstrip("-")
                number = phonenumbers.parse(phone_str, "US")
                if not phonenumbers.is_valid(number):
                    return "Null"
                return str(number.national_number)
        except Exception:
            return "Null"
    def process_series(chunk_data):
        series_obj = pd.Series(chunk_data)
        return series_obj.apply(parse_single_phone)
    
    raw_chunks = np.array_split(df["Phone"].values, 8)
    
    processed_chunks = Parallel(n_jobs=-1)(delayed(process_series)(c) for c in raw_chunks)
    combined_series = pd.concat(processed_chunks)
    combined_series.index = df.index
    df.loc[:, "Phone"] = combined_series
    return df

def standardise_sex(df: pd.DataFrame):
    allowed = ["m", "f"]
    clean_sx = df["Sex"].astype(str).str.strip().str.lower()
    mapping = {"m": "Male","male": "Male","f":"Female", "female": "Female",}
    df["Sex"] = clean_sx.map(mapping).fillna(df["Sex"])
    return df


def standardise_date(df: pd.DataFrame):
    df["Date of birth"] = pd.to_datetime(df["Date of birth"], errors='coerce').dt.strftime('%Y-%m-%d')
    return df


def drop_duplicates(df: pd.DataFrame, report: dict):
    duplicates = set(report.get("duplicates", []))
    try:
        df = df.drop(index=[i for i in duplicates if i in df.index])
        return df
    except Exception:
        raise

def clean(df: pd.DataFrame, report: dict):
    df = drop_duplicates(df, report)
    df = drop_invaldid_rows(df, report)
    df = fill_nulls(df, report)
    df = standardise_date(df)
    df = standardise_sex(df)
    df = standardise_phone(df)
    return df
    