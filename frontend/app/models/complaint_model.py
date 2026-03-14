from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class Complaint(BaseModel):
    id: Optional[str] = Field(default=None)
    description: str
    location: str
    image: Optional[str] = Field(default=None)
    category: Optional[str] = Field(default=None)
    priority: Optional[str] = Field(default="Medium")
    severity_score: Optional[int] = Field(default=0)
    department: Optional[str] = Field(default="City Administration")
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)
    status: Optional[str] = Field(default="Pending")
    created_at: Optional[str] = Field(default=None)
    
    model_config = ConfigDict(populate_by_name=True)