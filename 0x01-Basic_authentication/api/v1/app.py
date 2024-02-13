#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
auth_type = os.getenv("AUTH_TYPE")

if auth_type:
    from api.v1.auth.auth import Auth

    auth = Auth()

elif auth_type == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth

    auth = BasicAuth()


@app.before_request
def before_request() -> None:
    """
    Before request handler
    """
    if auth is None:
        return
    excluded_paths = [
        "/api/v1/status/", "/api/v1/unauthorized/", "/api/v1/forbidden/"
        ]
    if request.path not in excluded_paths:
        if auth.require_auth(request.path, excluded_paths):
            if not auth.authorization_header(request):
                abort(401)
            if not auth.current_user(request):
                abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """Not found handler"""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    new error handler for this status code

    Args:
        - a JSON: {"error": "Unauthorized"}
        - status code 401

    Returns:
        jsonify: 401 status code and the JSON
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    new error handler for this status code

    Args:
        - a JSON: {"error": "Forbidden"}
        - status code 403

    Returns:
        jsonify: 403 status code and the JSON
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
