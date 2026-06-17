import pandas as pd
import os


def extract_file(file_path: str):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    try:
        df = pd.read_csv(file_path) #*index_col=0
        if df.empty:
            raise ValueError("The provided file is empty.")
        columns = df.columns.tolist()
        expected_columns = {"Index", "User Id", "First Name", "Last Name", "Sex", "Email", "Phone", "Date of birth", "Job Title"}
        if not set([c.lower().strip() for c in expected_columns]).issubset(set([c.lower().strip() for c in columns])):
            missing = expected_columns - set(columns)
            raise ValueError(f"Missing required columns: {', '.join(missing)}")
        return df
    except pd.errors.EmptyDataError:
        raise ValueError("The provided file is empty.")
    except Exception as e:
        raise ValueError(f"Failed to parse CSV even with detected encoding: {e}")
    
