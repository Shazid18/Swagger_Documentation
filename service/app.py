from flask import Flask
from flask_restx import Api, Resource, fields
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Initialize Flask-RestX
api = Api(
    app,
    version='1.0',
    title='Integrate Swagger',
    description='A Swagger documentation of a User Management API.',
    doc='/swagger'
)

# Create a namespace
ns = api.namespace('api', description='API operations')

# Define models for request/response documentation
user_model = api.model('User', {
    'id': fields.Integer(readonly=True, description='User identifier'),
    'username': fields.String(required=True, description='Username'),
    'email': fields.String(required=True, description='User email'),
    'created_at': fields.DateTime(readonly=True, description='Creation timestamp')
})

# Sample data storage
users = []

@ns.route('/users')
class UserList(Resource):
    @ns.doc(
        description='Get all users profile'
    )
    @ns.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        return users

    @ns.doc(
            description='Create new user'
    )
    @ns.expect(user_model)
    @ns.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        user = api.payload
        user['id'] = len(users) + 1
        user['created_at'] = datetime.now()
        users.append(user)
        return user, 201

@ns.route('/users/<int:id>')
@ns.response(404, 'User not found')
@ns.param('id', 'The user identifier')
class User(Resource):
    @ns.doc(
            description='Get a specific user by ID'
    )
    @ns.marshal_with(user_model)
    def get(self, id):
        """Fetch a user by ID"""
        for user in users:
            if user['id'] == id:
                return user
        api.abort(404, f"User {id} doesn't exist")

    @ns.doc(
            description='Delete a specific user by ID'
    )
    @ns.response(204, 'User deleted')
    @ns.response(404, 'User not found')
    def delete(self, id):
        """Delete a user"""
        global users
        user_exists = any(user['id'] == id for user in users)
        if not user_exists:
            api.abort(404, f"User {id} doesn't exist")
        users = [user for user in users if user['id'] != id]
        return '', 204

    @ns.doc(
            description='Update user profile by giving updated informations and ID'
    )
    @ns.expect(user_model)
    @ns.marshal_with(user_model)
    def put(self, id):
        """Update a user"""
        for user in users:
            if user['id'] == id:
                user.update(api.payload)
                return user
        api.abort(404, f"User {id} doesn't exist")

if __name__ == '__main__':
    app.run(debug=True)