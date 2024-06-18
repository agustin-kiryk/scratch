import sys
import os
import uuid
import logging
from flask import Flask, jsonify, g, Response
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException

# Añadir el directorio src al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.Api_response import ApiResponse
from src.App_factory import create_app
from src.errorHandler.error_codes import codes
from src.errorHandler.error_handler import JSONErrorHandler

app = create_app()

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

@app.errorhandler(ValidationError)
def handle_validation_error(e):
    logger.error('Validation Error: %s', str(e), exc_info=True)
    return ApiResponse(message='Validation Error', code=codes.UNSUPPORTED_VALIDATION, data=str(e)).to_response()

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error('Internal Server Error: %s', str(e), exc_info=True)
    return ApiResponse(message='Internal Server Error', code=codes.INTERNAL_SERVER_ERROR, data=str(e)).to_response()

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
