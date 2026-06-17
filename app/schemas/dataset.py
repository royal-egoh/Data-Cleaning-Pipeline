from pydantic import BaseModel, ConfigDict
from datetime import datetime, date

class DatasetStatusResponse(BaseModel):
    dataset_id: str
    filename: str
    status: str
    row_count: int | None = None
    uploaded_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
      

class DatasetRowResponse(BaseModel):
    row_id: str
    dataset_id: str
    row_index: int
    
    user_id_field: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    sex: str | None = None
    email: str | None = None
    phone: str | None = None
    date_of_birth: date | None = None
    job_title: str | None = None
    # remark: str |None = None
    
    model_config = ConfigDict(from_attributes=True)


