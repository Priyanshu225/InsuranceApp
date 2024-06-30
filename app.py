from flask import Flask, request, jsonify
from crud_operations import (
    create_policyholder, read_policyholder, update_policyholder, delete_policyholder,
    create_policy, read_policy, update_policy, delete_policy,
    create_claim, read_claim, update_claim, delete_claim
)

app = Flask(__name__)

# Policyholder Endpoints
@app.route('/policyholders', methods=['POST'])
def api_create_policyholder():
    data = request.json
    policyholder = create_policyholder(data)
    if policyholder:
        return jsonify(policyholder.dict()), 201
    else:
        return jsonify({"error": "Invalid data"}), 400

@app.route('/policyholders/<int:policyholder_id>', methods=['GET'])
def api_read_policyholder(policyholder_id):
    policyholder = read_policyholder(policyholder_id)
    if policyholder:
        return jsonify(policyholder.dict()), 200
    else:
        return jsonify({"error": "Policyholder not found"}), 404

from flask import jsonify, request

@app.route('/policyholders/<int:policyholder_id>', methods=['PUT'])
def api_update_policyholder(policyholder_id):
    data = request.get_json()
    updated_policyholder = update_policyholder(policyholder_id, data)
    if updated_policyholder:
        # Convert Policyholder object to a serializable dictionary
        policyholder_dict = {
            'policyholder_id': updated_policyholder.policyholder_id,
            'name': updated_policyholder.name,
            'address': updated_policyholder.address,
            'contact_info': updated_policyholder.contact_info,
            # Add other fields as needed
        }
        return jsonify({'message': 'Policyholder updated successfully', 'policyholder': policyholder_dict}), 200
    else:
        return jsonify({'message': 'Failed to update policyholder'}), 500


@app.route('/policyholders/<int:policyholder_id>', methods=['DELETE'])
def api_delete_policyholder(policyholder_id):
    if delete_policyholder(policyholder_id):
        return jsonify({'message': 'Policy deleted successfully'})
    else:
        return jsonify({"error": "Policyholder not found"}), 404

# Policy Endpoints
@app.route('/policies', methods=['POST'])
def api_create_policy():
    try:
        policy_data = request.json
        created_policy = create_policy(policy_data)
        return jsonify(created_policy.dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/policies/<int:policy_id>', methods=['GET'])
def api_get_policy(policy_id):
    policy = read_policy(policy_id)
    if policy:
        return jsonify(policy.dict())
    return jsonify({'error': 'Policy not found'}), 404

@app.route('/policies/<int:policy_id>', methods=['PUT'])
def api_update_policy(policy_id):
    try:
        update_data = request.json
        updated_policy = update_policy(policy_id, update_data)
        if updated_policy:
            return jsonify(updated_policy.dict())
        return jsonify({'error': 'Policy not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/policies/<int:policy_id>', methods=['DELETE'])
def api_delete_policy(policy_id):
    deleted = delete_policy(policy_id)
    if deleted:
        return jsonify({'message': 'Policy deleted successfully'})
    return jsonify({'error': 'Policy not found'}), 404

# Claim Endpoints
@app.route('/claims', methods=['POST'])
def api_create_claim():
    data = request.json
    try:
        claim = create_claim(data)
        if claim:
            return jsonify(claim.dict()), 201
        else:
            return jsonify({"error": "Failed to create claim"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/claims/<int:claim_id>', methods=['GET'])
def api_read_claim(claim_id: int):
    try:
        claim = read_claim(claim_id)
        if claim:
            return jsonify(claim.dict()), 200
        else:
            return jsonify({"error": "Claim not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/claims/<int:claim_id>', methods=['PUT'])
def api_update_claim(claim_id: int):
    try:
        data = request.json
        updated_claim = update_claim(claim_id, data)
        if updated_claim:
            return jsonify(updated_claim.dict()), 200
        else:
            return jsonify({"error": "Claim not found or update failed"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/claims/<int:claim_id>', methods=['DELETE'])
def api_delete_claim(claim_id: int):
    try:
        success = delete_claim(claim_id)
        if success:
            return jsonify({"message": "Claim deleted successfully"}), 200
        else:
            return jsonify({"error": "Claim not found or deletion failed"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
