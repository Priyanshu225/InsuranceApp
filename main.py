# insurance_app/main.py

from crud_operations import (
    create_policyholder, read_policyholder, update_policyholder, delete_policyholder,
    create_policy, read_policy, update_policy, delete_policy,
    create_claim, read_claim, update_claim, delete_claim
)

def main():
    # Test Policyholder CRUD operations
    policyholder_data = {'policyholder_id': 1, 'name': 'John Doe', 'address': '123 Elm Street', 'contact_info': '555-1234'}
    policyholder = create_policyholder(policyholder_data)
    print(read_policyholder(1))

    update_policyholder(1, {'address': '456 Oak Street'})
    print(read_policyholder(1))

    delete_policyholder(1)
    print(read_policyholder(1))

    # Test Policy CRUD operations
    policy_data = {'policy_id': 1, 'policyholder_id': 1, 'policy_type': 'Auto', 'start_date': '2021-01-01', 'end_date': '2022-01-01', 'premium_amount': 1200.0}
    policy = create_policy(policy_data)
    print(read_policy(1))

    update_policy(1, {'premium_amount': 1300.0})
    print(read_policy(1))

    delete_policy(1)
    print(read_policy(1))

    # Test Claim CRUD operations
    claim_data = {'claim_id': 1, 'policy_id': 1, 'claim_date': '2021-06-01', 'claim_amount': 5000.0, 'status': 'Pending'}
    claim = create_claim(claim_data)
    print(read_claim(1))

    update_claim(1, {'status': 'Approved'})
    print(read_claim(1))

    delete_claim(1)
    print(read_claim(1))

    # Test validations
    invalid_policy_data = {'policy_id': 2, 'policyholder_id': 1, 'policy_type': 'Auto', 'start_date': '2022-01-01', 'end_date': '2021-01-01', 'premium_amount': 1200.0}
    create_policy(invalid_policy_data)

    invalid_claim_data = {'claim_id': 2, 'policy_id': 1, 'claim_date': '2021-06-01', 'claim_amount': -5000.0, 'status': 'Pending'}
    create_claim(invalid_claim_data)

if __name__ == "__main__":
    main()
