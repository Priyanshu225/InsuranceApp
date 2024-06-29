# insurance_app/test_entities.py

import unittest
from policyholder import Policyholder
from policy import Policy
from claim import Claim
from datetime import date
from pydantic import ValidationError

class TestEntities(unittest.TestCase):

    def test_policyholder_valid(self):
        policyholder = Policyholder(policyholder_id=1, name="John Doe", address="123 Elm Street", contact_info="555-1234")
        self.assertEqual(policyholder.name, "John Doe")

    def test_policyholder_invalid(self):
        with self.assertRaises(ValidationError):
            Policyholder(policyholder_id=-1, name="", address="", contact_info="")

    def test_policy_valid(self):
        policy = Policy(policy_id=1, policyholder_id=1, policy_type="Auto", start_date=date(2021, 1, 1), end_date=date(2022, 1, 1), premium_amount=1200.0)
        self.assertEqual(policy.policy_type, "Auto")

    def test_policy_invalid(self):
        with self.assertRaises(ValidationError):
            Policy(policy_id=0, policyholder_id=-1, policy_type="InvalidType", start_date="2021-01-01", end_date="2022-01-01", premium_amount=-100)

    def test_claim_valid(self):
        claim = Claim(claim_id=1, policy_id=1, claim_date=date(2021, 6, 1), claim_amount=5000.0, status="Pending")
        self.assertEqual(claim.status, "Pending")

    def test_claim_invalid(self):
        with self.assertRaises(ValidationError):
            Claim(claim_id=-1, policy_id=-1, claim_date="2021-06-01", claim_amount=-5000, status="InvalidStatus")

if __name__ == "__main__":
    unittest.main()
