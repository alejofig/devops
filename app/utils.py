from functools import wraps
import os 
from flask import request, jsonify

STATIC_TOKEN = os.getenv("STATIC_TOKEN")

def require_static_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token and token == f'Bearer {STATIC_TOKEN}':
            return func(*args, **kwargs)
        return jsonify({'message': 'Acceso no autorizado'}), 401
    return wrapper