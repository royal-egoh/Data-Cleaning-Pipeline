from celery import Celery
from dotenv import load_dotenv
load_dotenv()
import pandas as pd
from fastapi import HTTPException, status
from app.pipeline.cleaner import *
from app.pipeline.extractor import *
from app.pipeline.transformer import *
from app.pipeline.validator import *
from app.services.dataset_service import *
from app.models.user import User
from app.models.dataset import Dataset, DatasetRows
from app.database import SessionLocal
from sqlalchemy import select


celery_app = Celery('app', broker="redis://localhost:6379/0",
                    backend="redis://localhost:6379/0")

@celery_app.task
def data_pipeline(file_path: str, dataset_id: str):
    db = SessionLocal()
    dataset_file = None
    try:
        dataset_file = db.execute(select(Dataset).where(dataset_id==Dataset.dataset_id)).scalar_one_or_none()
        if dataset_file:
            dataset_file.status= "Processing"
            db.commit()
        df = extract_file(file_path)
        validator = validate(df)
        cleaner = clean(df, validator)
        transformed = transform(cleaner)
        load(transformed, dataset_id)
        dataset_file.status= "Completed"
        dataset_file.row_count = len(pd.read_csv(dataset_file.filename))
        db.commit()
        return f"{dataset_id} processed"
    except:
        db.rollback()
        if dataset_file:
            dataset_file.status="Failed"
            db.commit()
        raise ValueError("An error occured")
    finally:
        db.close()

