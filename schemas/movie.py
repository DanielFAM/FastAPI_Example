from pydantic import BaseModel, Field
from typing import Optional

class Movie(BaseModel):
    id: Optional[int] | None  = None
    title: str = Field(min_length=5, max_length=15) #validate object parameters with Field
    overview: str = Field(min_length=15, max_length=50)
    year:int = Field(le=2023)
    rating:float = Field(ge=1, le=10)
    category: str = Field(min_length=5, max_length=15)

    class Config:
        schema_extra = {
            "example":{
                "id":1,
                "title":"My movie",
                "overview":"Film description",
                "year":2022,
                "rating":9.8,
                "category":"Acción"
            }
        }