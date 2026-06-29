from fastapi import HTTPException, status, Depends, APIRouter, Request, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.models.user import User
from app.models.dataset import Dataset, DatasetRows
import shutil
from app.schemas.dataset import DatasetStatusResponse, DatasetRowResponse
from app.services.user_service import *
from app.schemas.user import *
from app.pipeline.cleaner import *
from app.pipeline.extractor import *
from app.pipeline.transformer import *
from app.pipeline.validator import *
from app.services.dataset_service import *
from io import StringIO
from pathlib import Path
from app.workers.pipeline_worker import data_pipeline
router = APIRouter(prefix="/pipeline")

UPLOAD_DIR = Path("app/test_files")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload")
async def upload_file(request: Request, file: UploadFile, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You do not own this file")
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as tosave:
        shutil.copyfileobj(file.file, tosave)
        
    new_file = str(file_path.resolve())
    
    new_dataset = create_dataset_record(filename=new_file,
                          user_id=current_user.id, db=db)

    cleaned_id = data_pipeline.delay(new_file, new_dataset.dataset_id)

    return new_dataset.dataset_id


@router.get("/dataset-status/{dataset_id}")
async def dataset_status(dataset_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    data = db.execute(select(Dataset).where(
        dataset_id == Dataset.dataset_id)).scalar_one_or_none()
    if current_user.id != data.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You do not own this file")
    if not data:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="No file found")

    return data.status


@router.get("/view-dataset-rows/{dataset_id}")
async def view_dataset_rows(dataset_id: str, page: int = 1,  db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = db.execute(select(Dataset).where(
        Dataset.user_id == current_user.id)).scalar_one_or_none() 
    if not data:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="No file found")
    
    return get_dataset_rows(dataset_id=dataset_id, db=db, user_id=current_user.id, page=page)
    
@router.get("/view-dataset")
async def view_dataset(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = db.execute(select(Dataset).where(
        Dataset.user_id == current_user.id)).scalar_one_or_none() 
    return get_user_datasets(user_id=current_user.id, db=db)

# @router.get("/view-dataset/{dataser_id}")~
# async def view_dataset_by_id():
#     pass

@router.get("/export-dataset")
async def export_dataset_file(dataset_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    data = db.execute(select(Dataset).where(
        Dataset.user_id == current_user.id)).scalar_one_or_none()
    if not data:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="No file found")
    return export_dataset(dataset_id, db, current_user.id)
