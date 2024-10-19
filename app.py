import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token
from urllib.parse import quote
from models import db, User, Role

app = Flask(__name__)

# Configure MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')


db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Signup
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    hashed_password = quote(data['password'])
    user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=hashed_password,
        role_id=data['role_id']
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

# Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and quote(user.password, data['password']):
        token = create_access_token(identity=user.id)
        return jsonify({"token": token}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/roles', methods=['POST'])
def create_role():
    data = request.json
    role = Role(role_name=data['role_name'], access_modules=data.get('access_modules', []))
    db.session.add(role)
    db.session.commit()
    return jsonify({"message": "Role created successfully"}), 201

@app.route('/roles', methods=['GET'])
def get_roles():
    roles = Role.query.all()
    return jsonify([{"id": role.id, "role_name": role.role_name, "access_modules": role.access_modules} for role in roles]), 200

# Update Role
@app.route('/roles/<int:role_id>', methods=['PUT'])
def update_role(role_id):
    data = request.json
    role = Role.query.get(role_id)
    if role:
        role.role_name = data['role_name']
        role.access_modules = data.get('access_modules', role.access_modules)
        db.session.commit()
        return jsonify({"message": "Role updated successfully"}), 200

@app.route('/roles/<int:role_id>', methods=['DELETE'])
def delete_role(role_id):
    role = Role.query.get(role_id)
    if not role:
        return jsonify({"message": "Role not found"}), 404
    db.session.delete(role)
    db.session.commit()

@app.route('/users/update_lastname', methods=['PUT'])
def update_users_lastname():
    data = request.json
    User.query.update({User.last_name: data['new_last_name']})
    db.session.commit()
    return jsonify({"message": "All last_names updated successfully"}), 200

@app.route('/users/search', methods=['GET'])
def search_users():
    query = request.args.get('query', '')
    users = User.query.filter(User.first_name.ilike(f'%{query}%') | User.last_name.ilike(f'%{query}%')).all()
    return jsonify([{"first_name": user.first_name, "last_name": user.last_name, "email": user.email} for user in users]), 200

if __name__ == '__main__':
    app.run(debug=True)