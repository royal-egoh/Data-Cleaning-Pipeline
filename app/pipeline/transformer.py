import pandas as pd
from app.models.dataset import Dataset, DatasetRows
from app.database import engine
from sqlalchemy.orm import Session

def transform(df: pd.DataFrame):
    df.loc[:, "Index"] = df["Index"].astype(int)
    df.loc[:, "User Id"] = df["User Id"].astype(str)
    df.loc[:, "First Name"] = df["First Name"].astype(str)
    df.loc[:, "Last Name"] = df["Last Name"].astype(str)
    df.loc[:, "Sex"] = df["Sex"].astype(str)
    df.loc[:, "Email"] = df["Email"].astype(str)
    df.loc[:, "Phone"] = df["Phone"].astype(str)
    df.loc[:, "Job Title"] = df["Job Title"].astype(str)
    df = df.rename(columns={"Index":"row_index", "User Id": "user_id_field",
                            "First Name":"first_name", "Last Name":"last_name", "Sex":"sex", 
                            "Email":"email", "Phone":"phone", "Date of birth":"date_of_birth", "Job Title":"job_title"})
    return df
    
def load(df: pd.DataFrame, dataset_id: str):
    df["dataset_id"] = dataset_id
    df.to_sql(
        name="datasetrows",
        con=engine,
        if_exists="append",
        index=False,
        chunksize=5000,
        method="multi"
    )

    