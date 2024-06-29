# insurance_app/claim.py

from pydantic import BaseModel, Field, validator
from datetime import date
from typing import Literal

class Claim(BaseModel):
    claim_id: int = Field(..., gt=0, description="Claim ID must be a positive integer")
    policy_id: int = Field(..., gt=0, description="Policy ID must be a positive integer")
    claim_date: date = Field(..., description="Date of the claim")
    claim_amount: float = Field(..., gt=0, description="Claim amount must be a positive number")
    status: Literal['Pending', 'Approved', 'Rejected'] = Field(..., description="Status of the claim")

    def __repr__(self):
        return f"Claim({self.claim_id}, {self.policy_id}, {self.claim_date}, {self.claim_amount}, {self.status})"
