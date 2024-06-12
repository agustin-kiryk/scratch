import sys
import os
import uuid

from flask import Flask, jsonify, g, Response
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException

# Añadir el directorio src al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import ApiResponse
from src.App_factory import create_app
from src.error_handler import JSONErrorHandler

app = create_app()

@app.errorhandler(ValidationError)
def handle_validation_error(e):
    return ApiResponse(message='Validation Error', code=400, data=str(e)).to_response()

@app.errorhandler(Exception)
def handle_exception(e):
    return ApiResponse(message='Internal Server Error', code=500, data=str(e)).to_response()

@app.before_request
def generate_request_id():
    request_id = str(uuid.uuid4())
    g.request_id = request_id

@app.after_request
def attach_request_id(response):
    response.headers["X-Request-ID"] = g.get("request_id", "")
    return response

@app.teardown_request
def teardown_request(exception=None):
    g.pop("request_id", None)
    
    
@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
