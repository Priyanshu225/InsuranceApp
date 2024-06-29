# insurance_app/app.py

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

@app.route('/policyholders/<int:policyholder_id>', methods=['PUT'])
def api_update_policyholder(policyholder_id):
    data = request.json
    policyholder = update_policyholder(policyholder_id, data)
    if policyholder:
        return jsonify(policyholder.dict()), 200
    else:
        return jsonify({"error": "Policyholder not found"}), 404

@app.route('/policyholders/<int:policyholder_id>', methods=['DELETE'])
def api_delete_policyholder(policyholder_id):
    if delete_policyholder(policyholder_id):
        return '', 204
    else:
        return jsonify({"error": "Policyholder not found"}), 404

# Policy Endpoints
@app.route('/policies', methods=['POST'])
def api_create_policy():
    data = request.json
    policy = create_policy(data)
    if policy:
        return jsonify(policy.dict()), 201
    else:
        return jsonify({"error": "Invalid data"}), 400

@app.route('/policies/<int:policy_id>', methods=['GET'])
def api_read_policy(policy_id):
    policy = read_policy(policy_id)
    if policy:
        return jsonify(policy.dict()), 200
    else:
        return jsonify({"error": "Policy not found"}), 404

@app.route('/policies/<int:policy_id>', methods=['PUT'])
def api_update_policy(policy_id):
    data = request.json
    policy = update_policy(policy_id, data)
    if policy:
        return jsonify(policy.dict()), 200
    else:
        return jsonify({"error": "Policy not found"}), 404

@app.route('/policies/<int:policy_id>', methods=['DELETE'])
def api_delete_policy(policy_id):
    if delete_policy(policy_id):
        return '', 204
    else:
        return jsonify({"error": "Policy not found"}), 404

# Claim Endpoints
@app.route('/claims', methods=['POST'])
def api_create_claim():
    data = request.json
    claim = create_claim(data)
    if claim:
        return jsonify(claim.dict()), 201
    else:
        return jsonify({"error": "Invalid data"}), 400

@app.route('/claims/<int:claim_id>', methods=['GET'])
def api_read_claim(claim_id):
    claim = read_claim(claim_id)
    if claim:
        return jsonify(claim.dict()), 200
    else:
        return jsonify({"error": "Claim not found"}), 404

@app.route('/claims/<int:claim_id>', methods=['PUT'])
def api_update_claim(claim_id):
    data = request.json
    claim = update_claim(claim_id, data)
    if claim:
        return jsonify(claim.dict()), 200
    else:
        return jsonify({"error": "Claim not found"}), 404

@app.route('/claims/<int:claim_id>', methods=['DELETE'])
def api_delete_claim(claim_id):
    if delete_claim(claim_id):
        return '', 204
    else:
        return jsonify({"error": "Claim not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
