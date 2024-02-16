#!/usr/bin/env python3
""" Module of session auth views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """
    Handle user login and session creation.

    This route handles the user login process by receiving the email and
    password parameters from the request form data. It validates the provided
    credentials and creates a session ID for the authenticated user.

    Returns:
        Flask.Response: A JSON response containing the user data if login is
        successful, along with a session cookie containing the session ID.
    """
    user_email = request.form.get("email")
    user_password = request.form.get("password")

    # Check if email and password are provided
    if not user_email:
        return jsonify({"error": "email missing"}), 400
    if not user_password:
        return jsonify({"error": "password missing"}), 400

    # Retrieve user by email
    user = User.search({"email": user_email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    # Check if password is valid
    if not user.is_valid_password(user_password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)

    # Retrieve session name from environment variable or use a default value
    session_name = getenv("SESSION_NAME", "_my_session_id")

    # Create response with user data
    response_dict = jsonify(user.to_dict())

    # Set session cookie
    response = make_response(response_dict)
    response.set_cookie(session_name, session_id)

    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def session_logout():
    """
    Handle user logout and session deletion.

    This route handles the user logout process by deleting the session ID
    associated with the user. It also clears the session cookie from the
    response.

    Returns:
        Flask.Response: An empty JSON response with a cleared session cookie.
    """
    from api.v1.app import auth
    # Check if session ID is valid
    if not auth.destroy_session(request):
        abort(404)

    # Create empty response
    response = make_response(jsonify({}), 200)

    return response
