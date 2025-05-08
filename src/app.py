"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")

initial_members = [{"nombre": "John", "age": 33, "lucky_numbers":[7,13,22] },
                   {"nombre": "Jane", "age": 35, "lucky_numbers":[10,14,3] },
                   {"nombre": "Jimmy", "age": 5, "lucky_numbers":[1] }]



# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_members():
    return jsonify(jackson_family.get_all_members()), 200

@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    return jsonify({"error": "Member not found"}), 404

@app.route('/members', methods=['POST'])
def add_member():
    data = request.get_json()
    if "first_name" not in data or "age" not in data or "lucky_numbers" not in data:
        return jsonify({"error": "Missing data"}), 400
    new_member = jackson_family.add_member(data)
    return jsonify(new_member), 200

@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    if jackson_family.delete_member(member_id):
        return jsonify({"done": True}), 200
    return jsonify({"error": "Member not found"}), 404


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
