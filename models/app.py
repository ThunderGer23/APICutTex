from typing import List
from pydantic import BaseModel

class Files(BaseModel):
    id: List[str]