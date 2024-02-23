#!/usr/bin/env python3
"""
Main Module -- End-to-end integration test
"""
import requests

BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """
    Register a user with the given email and password.

    Args:
        email (str): The email of the user to register.
        password (str): The password of the user to register.

    Returns:
        None

    Raises:
        AssertionError: If the registration fails.
    """
    url = f"{BASE_URL}/register"
    data = {"email": email, "password": password}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise AssertionError(f"Failed to register user: {err}") from err


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Attempt to log in with the wrong password.

    Args:
        email (str): The email of the user.
        password (str): The incorrect password.

    Returns:
        None

    Raises:
        AssertionError: If the login does not fail with a 401 status code.
    """
    url = f"{BASE_URL}/login"
    data = {"email": email, "password": password}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        assert response.status_code == 401, \
            f"Expected status code 401, got {response.status_code}"


def log_in(email: str, password: str) -> str:
    """
    Log in a user with the given email and password.

    Args:
        email (str): The email of the user to log in.
        password (str): The password of the user to log in.

    Returns:
        str: The session ID.

    Raises:
        AssertionError: If the login fails.
    """
    url = f"{BASE_URL}/login"
    data = {"email": email, "password": password}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.cookies.get("session_id")
    except requests.exceptions.HTTPError as err:
        raise AssertionError(f"Failed to log in: {err}") from err


def profile_unlogged() -> None:
    """
    Access the profile page while not logged in.

    Returns:
        None

    Raises:
        AssertionError: If accessing the profile page does not fail with a
        403 status code.
    """
    url = f"{BASE_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 403, \
        f"Expected status code 403, got {response.status_code}"


def profile_logged(session_id: str) -> None:
    """
    Access the profile page while logged in.

    Args:
        session_id (str): The session ID of the logged-in user.

    Returns:
        None

    Raises:
        AssertionError: If accessing the profile page fails.
    """
    url = f"{BASE_URL}/profile"
    cookies = {"session_id": session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """
    Log out the user with the given session ID.

    Args:
        session_id (str): The session ID of the user to log out.

    Returns:
        None

    Raises:
        AssertionError: If logging out fails.
    """
    url = f"{BASE_URL}/logout"
    cookies = {"session_id": session_id}
    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """
    Get the reset password token for the user with the given email.

    Args:
        email (str): The email of the user.

    Returns:
        str: The reset password token.

    Raises:
        AssertionError: If getting the reset password token fails.
    """
    url = f"{BASE_URL}/reset_password"
    data = {"email": email}
    response = requests.post(url, data=data)
    assert response.status_code == 200, \
        f"Failed to get reset password token: {response.text}"
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Update password for the user with the given email using the reset token.

    Args:
        email (str): The email of the user.
        reset_token (str): The reset password token.
        new_password (str): The new password for the user.

    Returns:
        None

    Raises:
        AssertionError: If updating the password fails.
    """
    url = f"{BASE_URL}/reset_password"
    data = {"email": email, "reset_token":
            reset_token, "new_password": new_password}
    response = requests.put(url, data=data)
    assert response.status_code == 200, \
        f"Failed to update password: {response.text}"


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
