from pydantic import BaseModel, Field
from typing import Optional, List

class Item(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    description: Optional[str] = Field(None, max_length=300)
    price: float = Field(..., gt=0)
    tag: List[str] = Field(default=[], alias="item-tags")