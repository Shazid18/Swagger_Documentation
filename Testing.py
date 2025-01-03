# Import required libraries
from flask import Flask 
# Flask is the main web framework that handles HTTP requests and responses

from flask_restx import Api, Resource, fields
# flask_restx is an extension that adds support for quickly building REST APIs
# - Api: Main class for creating REST API
# - Resource: Base class for creating API endpoints
# - fields: Used for request/response data validation and documentation

from datetime import datetime
# Used for timestamp creation when creating users

# Create Flask application instance
app = Flask(__name__)
# __name__ is a special Python variable that holds the name of the current module

# Initialize Flask-RestX with API metadata
api = Api(
    app,                    # Flask app instance
    version='1.0',         # API version number
    title='Integrate Swagger',  # API title shown in Swagger UI
    description='A Swagger documentation of an existing Flask application.',  # API description
    doc='/swagger'         # URL path where Swagger UI will be available
)

# Create a namespace for API routes
ns = api.namespace('api', description='API operations')
# Namespaces help organize APIs into logical groups
# All routes in this namespace will be prefixed with /api

# Define the data model for users
user_model = api.model('User', {
    'id': fields.Integer(readonly=True, description='User identifier'),
    # Integer field, read-only (client can't set it), used as unique identifier
    
    'username': fields.String(required=True, description='Username'),
    # String field, required in requests
    
    'email': fields.String(required=True, description='User email'),
    # String field, required in requests
    
    'created_at': fields.DateTime(readonly=True, description='Creation timestamp')
    # DateTime field, read-only, automatically set when user is created
})

# Initialize empty list to store users (in-memory storage)
users = []

# Define endpoint for collection of users (/api/users)
@ns.route('/users')
class UserList(Resource):
    @ns.doc('list_users')  # Documentation for this endpoint
    @ns.marshal_list_with(user_model)  # Format response using user_model
    def get(self):
        """List all users"""
        return users  # Return all users

    @ns.doc('create_user')  # Documentation for this endpoint
    @ns.expect(user_model)  # Expect request body to match user_model
    @ns.marshal_with(user_model, code=201)  # Format response and set 201 status code
    def post(self):
        """Create a new user"""
        user = api.payload  # Get request body
        user['id'] = len(users) + 1  # Generate new ID
        user['created_at'] = datetime.utcnow()  # Set creation timestamp
        users.append(user)  # Add user to storage
        return user, 201  # Return created user with 201 status code

# Define endpoint for individual users (/api/users/<id>)
@ns.route('/users/<int:id>')
@ns.response(404, 'User not found')  # Document possible 404 response
@ns.param('id', 'The user identifier')  # Document ID parameter
class User(Resource):
    @ns.doc('get_user')
    @ns.marshal_with(user_model)
    def get(self, id):
        """Fetch a user by ID"""
        for user in users:
            if user['id'] == id:  # Find user with matching ID
                return user
        api.abort(404, f"User {id} doesn't exist")  # Return 404 if not found

    @ns.doc('delete_user')
    @ns.response(204, 'User deleted')
    @ns.response(404, 'User not found')
    def delete(self, id):
        """Delete a user"""
        global users  # Reference global users list
        user_exists = any(user['id'] == id for user in users)  # Check if user exists
        if not user_exists:
            api.abort(404, f"User {id} doesn't exist")  # Return 404 if not found
        users = [user for user in users if user['id'] != id]  # Remove user with matching ID
        return '', 204  # Return empty response with 204 status code

    @ns.doc('update_user')
    @ns.expect(user_model)  # Expect request body to match user_model
    @ns.marshal_with(user_model)
    def put(self, id):
        """Update a user"""
        for user in users:
            if user['id'] == id:  # Find user with matching ID
                user.update(api.payload)  # Update user data
                return user
        api.abort(404, f"User {id} doesn't exist")  # Return 404 if not found

# Run the application if this file is executed directly
if __name__ == '__main__':
    app.run(debug=True)  # Start development server with debug mode