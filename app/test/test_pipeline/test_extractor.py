import pandas as pd
from app.pipeline.extractor import *
import os

def test_extractor():
    file_path = "app/test_files/people-100.csv"
    
    df = extract_file(file_path)
    expected = ["Index", "User Id", "First Name", "Last Name", "Sex", "Email", "Phone", "Date of birth", "Job Title"]
    assert df.columns.tolist() == expected
    