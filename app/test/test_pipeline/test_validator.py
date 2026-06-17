import pandas as pd
from app.pipeline.validator import *

def test_check_email():
    df = pd.DataFrame({
        "Email": ["royalegoh@gmail.com", "iunew cj j", "123", "Aodsb@ddg.com"]
    })
    result = check_emails(df)
    assert result==[1, 2]
    
# def test
    
