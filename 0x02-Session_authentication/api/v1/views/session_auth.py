#!/usr/bin/env python3
"""
This module implements Session Authentication using Flask.
"""

from flask import (
    request,
    jsonify,
    abort
)
from os import getenv

from api.v1.views import app_views
from models.user import User
from api.v1.auth.session_auth import SessionAuth


@app_views.route(
    "/auth_session/login",
    strict_slashes=False,
    methods=["POST"]
)
def login():
    """
    Handle user login requests and create a session.

    Returns:
        JSON: Response containing user information on successful login.
              Otherwise, returns error messages with appropriate status codes.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    # Check for valid user email
    if not email or email == "":
        return jsonify({"error": "email missing"}), 400

    # Check for valid password
    if not password or password == "":
        return jsonify({"error": "password missing"}), 400

    # Verify user's email address
    list_of_users = User.search({"email": email})
    if len(list_of_users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    # Verify user's password
    user = list_of_users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create a new session for the user
    new_session_id = auth.create_session(user.id)

    # Obtain response object so session cookie can be added to the response
    response = jsonify(user.to_json())
    response.set_cookie(getenv("SESSION_NAME"), new_session_id)

    return response


@app_views.route(
    "/auth_session/logout",
    strict_slashes=False,
    methods=["DELETE"]
)
def logout():
    """
    Handle user logout requests.

    Returns:
        JSON: Empty response with 200 status code upon successful logout.
              Otherwise, returns error message with 404 status code.
    """
    # Destroy user's session
    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200
