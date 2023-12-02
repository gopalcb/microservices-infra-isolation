"""
manage application auth
"""
import datetime
from flask import Flask, request, jsonify, make_response
from  werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime, timedelta
from dynamo_db import DynamoDB
from log import log

class Auth:
    dynamodb = DynamoDB()

    def __init__(self, app) -> None:
        self.app = app


    def login(self):
        """
        """
        auth_data = request.json
        email = auth_data.get('email')
        password = auth_data.get('password')
    
        if not auth_data or not email or not password:
            return make_response(
                'Could not verify', 401, {
                    'WWW-Authenticate' : 'Basic realm ="Login required !!"'
                }
            )
    
        # get user from dynamodb
        # user = {
        #     'id': 'user-id',
        #     'email': 'test@gmail.com',
        #     'password': 'pass'
        # }
        table = 'tenant'
        fetch_key={
            'email': {'S': email},
            'password': {'S': generate_password_hash(password)}  # hash the password
        }
        user = self.dynamodb.get_single_item(table, fetch_key)
    
        if not user:
            # returns 401 if user does not exist
            return make_response('Could not verify', 401, {
                    'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'
                }
            )
    
        if check_password_hash(user['password'], generate_password_hash(password)):
            # generates the JWT Token
            token = jwt.encode({
                'public_id': user['id'],
                'exp' : datetime.utcnow() + timedelta(minutes = 30)
            }, self.app.config['SECRET_KEY'])
    
            return make_response(jsonify({'token' : token.decode('UTF-8')}), 201)

        # returns 403 if password is wrong
        return make_response('Could not verify', 403,
            {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
        )
        
    
    def signup(self):
        """
        """
        data = request.json
    
        # gets name, email and password
        name, email = data.get('name'), data.get('email')
        password = data.get('password')
    
        # checking for existing user in dynamodb
        table = 'tenant'
        fetch_key={
            'email': {'S': email},
            'password': {'S': generate_password_hash(password)}  # hash the password
        }
        tenant = self.dynamodb.get_single_item(table, fetch_key)

        if not tenant:
            data['id'] = str(uuid.uuid4())
            self.dynamodb.save(data)
    
            return make_response('Successfully registered.', 201)
        
        return make_response('User already exists. Please Log in.', 202)
