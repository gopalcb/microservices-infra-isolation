"""
handle service routing
"""
import traceback
from functools import wraps
from flask import Flask, request, jsonify, make_response
import uuid
from  werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from log import log
from auth import Auth
from dynamo_db import DynamoDB

class Routing:
    dynamodb = DynamoDB()

    def __init__(self, app) -> None:
        self.app = app

    def serve(self):
        """
        routes block
        """

        # decorator for verifying the JWT
        def token_required(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                """
                """
                token = None
                # jwt is passed in the request header
                if 'x-access-token' in request.headers:
                    token = request.headers['x-access-token']

                # return 401 if token is not passed
                if not token:
                    return jsonify({'message' : 'Token is missing !!'}), 401
        
                try:
                    # decoding the payload to fetch the stored details
                    data = jwt.decode(token, self.app.config['SECRET_KEY'])
                    # here fetch from dynamodb user table
                    email, password = data['email'], data['password']
                    current_user = self.dynamodb.get_single_item('tenant', {
                        'email': {'S': email},
                        'password': {'S': generate_password_hash(password)}
                    })
                    if current_user:
                        pass
                    else:
                        return jsonify({
                        'message' : 'Token is invalid !!'
                    }), 401

                except Exception as e:
                    return jsonify({
                        'message' : 'Token is invalid !!'
                    }), 401
                
                # returns the current logged in users context to the routes
                return  f(current_user, *args, **kwargs)
        
            return decorated


        def prepare_return_object(status, payload=None):
            """
            prepare object to return from route
            """
            obj = {
                'status': status,
                'code': 200 if status else 500,
                'payload': payload
            }
            return obj
        

        @self.app.route('/', methods=['GET'])
        def index():
            """
            """
            return 'flask rest connected'
        

        # User Database Route
        # this route sends back list of users
        @self.app.route('/tenants', methods =['GET'])
        @token_required
        def get_all_users(current_user):
            """
            """
            users = []
            # converting the query objects
            # to list of jsons
            output = []
            for user in users:
                # appending the user data json 
                # to the response list
                output.append({
                    'public_id': user.public_id,
                    'name' : user.name,
                    'email' : user.email
                })
        
            return jsonify({'users': output})


        # route for logging user in
        @self.app.route('/login', methods =['POST'])
        def login():
            """
            """
            auth = Auth(self.app)
            return auth.login()
        

        # signup route
        @self.app.route('/signup', methods =['POST'])
        def signup():
            """
            """
            auth = Auth(self.app)
            return auth.signup()
