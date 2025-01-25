from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token
from models import db, Company, Tool, Section, Component

api_routes = Blueprint('api', __name__)

# Helper function to generate JWT token
def generate_token(company):
    return create_access_token(identity=company.id)

# Company registration (Sign up)
@api_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    company = Company(name=data['name'], email=data['email'], password=data['password'])
    db.session.add(company)
    db.session.commit()
    return jsonify(message="Company registered successfully"), 201

# User login
@api_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    company = Company.query.filter_by(email=data['email']).first()
    if company and company.password == data['password']:  # Use hashed passwords in production
        token = generate_token(company)
        return jsonify(access_token=token), 200
    return jsonify(message="Invalid credentials"), 401

# CRUD Operations for Tools
@api_routes.route('/tools', methods=['POST'])
@jwt_required()
def create_tool():
    data = request.get_json()
    company_id = get_jwt_identity()  # Get the company ID from JWT
    tool = Tool(name=data['name'], version=data['version'], company_id=company_id)
    db.session.add(tool)
    db.session.commit()
    return jsonify(message="Tool created successfully"), 201

@api_routes.route('/tools/<tool_id>', methods=['GET'])
def get_tool(tool_id):
    tool = Tool.query.get(tool_id)
    if not tool:
        return jsonify(message="Tool not found"), 404
    return jsonify(tool={"id": tool.id, "name": tool.name, "version": tool.version})

# Publish tool (change state to live)
@api_routes.route('/tools/<tool_id>/publish', methods=['PUT'])
@jwt_required()
def publish_tool(tool_id):
    tool = Tool.query.get(tool_id)
    if not tool:
        return jsonify(message="Tool not found"), 404
    tool.status = 'live'
    db.session.commit()
    return jsonify(message="Tool published successfully"), 200

# Estimate Calculation
@api_routes.route('/estimate', methods=['POST'])
def calculate_estimate():
    data = request.get_json()
    total_cost = 0
    for component_id in data['components']:
        component = Component.query.get(component_id)
        if component:
            total_cost += component.pricing
    return jsonify(total_cost=total_cost), 200
 
