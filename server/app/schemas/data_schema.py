from pydantic import BaseModel
from typing import List, Dict, Any

class DataEntry(BaseModel):
    data_category: str
    content: Dict[str, Any]

class UploadData(BaseModel):
    object_id: str
    session_id: str
    sender_data: Dict[str, Any]
    data: List[DataEntry]
