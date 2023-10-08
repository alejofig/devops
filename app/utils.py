from functools import wraps
import os 
from flask import request, jsonify

API_KEY = os.getenv("API_KEY")

def require_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.headers.get('x-api-key') == API_KEY:
            return func(*args, **kwargs)
        else:
            return jsonify({'message': 'Acceso no autorizado'}), 401
    return wrapper