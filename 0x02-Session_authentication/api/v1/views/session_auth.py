#!/usr/bin/env python3
""" Module of session auth views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Handle user login and session creation.

    This route handles the user login process by receiving the email and
    password. parameters from the request form data. It validates the provided
    credentials and creates a session ID for the authenticated user.

    Returns:
        Flask.Response: A JSON response containing the user data if login is
        successful, along with a session cookie containing the session ID.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    # Check if email and password are provided
    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400

    # Retrieve user by email
    user = User.search({"email": email})
    if user is None:
        return jsonify({"error": "no user found for this email"}), 404

    # Check if password is valid
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(getenv("SESSION_NAME"), session_id)
    return response
