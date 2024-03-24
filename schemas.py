from pydantic import BaseModel
from datetime import datetime

class Note(BaseModel):
    title           : str
    content         : str
    createdAt       : datetime = None