#!/usr/bin/env python3
"""
Basic Flask app
"""
from flask import Flask, jsonify, request, make_response, abort, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """
    Main route for the Flask app
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user() -> str:
    """
    Register a user

    Returns:
        str: JSON string

    Raises:
        ValueError: If the user already exists
    """
    # get the email and password from the data
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        # if the user does not exist, register the user
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        # if the user already exists, return a 400 error
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    Handle user login.

    - Expects a POST request with form data containing "email" and "password"
        fields.

    - Creates a new session for the user, stores the session ID as a cookie,
        and returns a JSON response.

    Returns:
        Flask response: JSON response confirming the login.

    Raises:
        - HTTPException: If login information is incorrect, aborts with a 401
            status code.
    """
    # get the email and password from the data
    email = request.form.get('email')
    password = request.form.get('password')

    # if the user exists and the password is valid, create a new session
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = make_response(jsonify({"email": email, "message":
                                          "logged in"}))
        response.set_cookie("session_id", session_id)
        return response
    # if the user does not exist or the password is invalid, return a 403 error
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """
    Handle user logout.

    - Deletes the user's session from the session_id cookie.

    Returns:
        str: JSON string
    """
    session_id = request.cookies.get("session_id")

    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)


@app.route('/profile')
def profile() -> str:
    """
    Get the user's profile

    Returns:
        str: JSON string
    """
    session_id = request.cookies.get("session_id")

    user_profile = AUTH.get_user_from_session_id(session_id)
    if user_profile:
        return jsonify({"email": user_profile.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    Get the reset password token

    Returns:
        str: JSON string
    """
    try:
        email = request.form.get('email')
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """
    Handle updating user password

    Returns:
        str: JSON string

    Raises:
        ValueError: If the reset token is invalid, aborts with a 403 status
        code.
    """
    # Get form data
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        # update the password
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
