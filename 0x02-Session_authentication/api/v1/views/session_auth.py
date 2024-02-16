#!/usr/bin/env python3
""" Module of session auth views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """
    Handle user login and session creation.

    This route handles the user login process by receiving the email and
    password. parameters from the request form data. It validates the provided
    credentials and creates a session ID for the authenticated user.

    Returns:
        Flask.Response: A JSON response containing the user data if login is
        successful, along with a session cookie containing the session ID.
    """
    user_email = request.form.get("email")
    user_password = request.form.get("password")

    # Check if email and password are provided
    if user_email is None or user_email == "":
        return jsonify({"error": "email missing"}), 400
    if user_password is None or user_password == "":
        return jsonify({"error": "password missing"}), 400

    # Retrieve user by email
    is_valid_user = User.search({"email": user_email})
    if not is_valid_user:
        return jsonify({"error": "no user found for this email"}), 404

    # Check if password is valid
    if not is_valid_user.is_valid_password(user_password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(is_valid_user.id)
    response_data = getenv(("SESSION_NAME"), session_id)
    response_dict = jsonify(is_valid_user.to_dict())
    return response_dict.set_cookie(response_data, session_id)
