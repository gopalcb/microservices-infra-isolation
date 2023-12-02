"""
"""
from flask import Flask, request, jsonify, make_response
import uuid
from  werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
from routing import Routing

app = Flask(__name__)
# set app secret key
app.config['SECRET_KEY'] = 'app-secret-key'

routing = Routing(app)
routing.serve()


if __name__ == '__main__':
    app.run(host="localhost", port=2000, debug=True)
