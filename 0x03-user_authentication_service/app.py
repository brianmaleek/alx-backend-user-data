#!/usr/bin/env python3
"""
Basic Flask app
"""
from flask import Flask, jsonify, request, make_response, abort
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)