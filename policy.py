# insurance_app/policy.py

from pydantic import BaseModel, Field, validator
from datetime import date
from typing import Literal

class Policy(BaseModel):
    policy_id: int = Field(..., gt=0, description="Policy ID must be a positive integer")
    policyholder_id: int = Field(..., gt=0, description="Policyholder ID must be a positive integer")
    policy_type: Literal['Auto', 'Home', 'Life'] = Field(..., description="Policy type must be either 'Auto', 'Home', or 'Life'")
    start_date: date = Field(..., description="Start date of the policy")
    end_date: date = Field(..., description="End date of the policy")
    premium_amount: float = Field(..., gt=0, description="Premium amount must be a positive number")

    @validator('end_date')
    def check_end_date(cls, v, values):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('End date must be after start date')
        return v

    def __repr__(self):
        return f"Policy({self.policy_id}, {self.policyholder_id}, {self.policy_type}, {self.start_date}, {self.end_date}, {self.premium_amount})"
