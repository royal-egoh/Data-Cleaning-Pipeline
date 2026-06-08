# What does a dataset upload response look like?
# What does a status check response look like?
# Do you need a create schema for datasets or does the file come through differently?

from pydantic import BaseModel, ConfigDict, EmailStr, model_validator, Field, StrictBool
from datetime import datetime

class DatasetCreate(BaseModel):
    pass

class DatasetResponse(BaseModel):
    pass

