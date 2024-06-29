# insurance_app/policyholder.py

from pydantic import BaseModel, Field
from typing import Optional

class Policyholder(BaseModel):
    policyholder_id: int = Field(..., gt=0, description="Policyholder ID must be a positive integer")
    name: str = Field(..., min_length=1, max_length=100, description="Name must be between 1 and 100 characters")
    address: str = Field(..., min_length=1, max_length=200, description="Address must be between 1 and 200 characters")
    contact_info: str = Field(..., min_length=1, max_length=15, description="Contact info must be between 1 and 15 characters")

    def __repr__(self):
        return f"Policyholder({self.policyholder_id}, {self.name}, {self.address}, {self.contact_info})"
