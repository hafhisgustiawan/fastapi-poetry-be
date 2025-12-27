from pydantic import BaseModel

from typing import Optional, List
from datetime import datetime

class Food(BaseModel):
    id : int
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
class GetFoodResponse(BaseModel):
    data: List[Optional[Food] | None]