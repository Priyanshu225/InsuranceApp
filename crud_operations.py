# insurance_app/crud_operations.py

from typing import Dict, List
from policyholder import Policyholder
from policy import Policy
from claim import Claim
from pydantic import ValidationError

# In-memory storage for records
policyholders: Dict[int, Policyholder] = {}
policies: Dict[int, Policy] = {}
claims: Dict[int, Claim] = {}

# Policyholder CRUD functions
def create_policyholder(policyholder_data: dict) -> Policyholder:
    try:
        policyholder = Policyholder(**policyholder_data)
        policyholders[policyholder.policyholder_id] = policyholder
        return policyholder
    except ValidationError as e:
        print(f"Error creating policyholder: {e}")
        return None

def read_policyholder(policyholder_id: int) -> Policyholder:
    return policyholders.get(policyholder_id)

def update_policyholder(policyholder_id: int, update_data: dict) -> Policyholder:
    policyholder = policyholders.get(policyholder_id)
    if policyholder:
        for key, value in update_data.items():
            setattr(policyholder, key, value)
        return policyholder
    return None

def delete_policyholder(policyholder_id: int) -> bool:
    if policyholder_id in policyholders:
        del policyholders[policyholder_id]
        return True
    return False

# Policy CRUD functions
def create_policy(policy_data: dict) -> Policy:
    try:
        policy = Policy(**policy_data)
        policies[policy.policy_id] = policy
        return policy
    except ValidationError as e:
        print(f"Error creating policy: {e}")
        return None

def read_policy(policy_id: int) -> Policy:
    return policies.get(policy_id)

def update_policy(policy_id: int, update_data: dict) -> Policy:
    policy = policies.get(policy_id)
    if policy:
        for key, value in update_data.items():
            setattr(policy, key, value)
        return policy
    return None

def delete_policy(policy_id: int) -> bool:
    if policy_id in policies:
        del policies[policy_id]
        return True
    return False

# Claim CRUD functions
def create_claim(claim_data: dict) -> Claim:
    try:
        claim = Claim(**claim_data)
        claims[claim.claim_id] = claim
        return claim
    except ValidationError as e:
        print(f"Error creating claim: {e}")
        return None

def read_claim(claim_id: int) -> Claim:
    return claims.get(claim_id)

def update_claim(claim_id: int, update_data: dict) -> Claim:
    claim = claims.get(claim_id)
    if claim:
        for key, value in update_data.items():
            setattr(claim, key, value)
        return claim
    return None

def delete_claim(claim_id: int) -> bool:
    if claim_id in claims:
        del claims[claim_id]
        return True
    return False
