#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None


auth = os.getenv("AUTH_TYPE")
""" Intialize auth instance based on authentication
type from environment variable.
"""
if auth:
    if auth == "basic_auth":
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()
    elif auth == "session_auth":
        from api.v1.auth.session_auth import SessionAuth
        auth = SessionAuth()
    elif auth == "session_exp_auth":
        from api.v1.auth.session_exp_auth import SessionExpAuth
        auth = SessionExpAuth()
    elif auth == "session_db_auth":
        from api.v1.auth.session_db_auth import SessionDBAuth
        auth = SessionDBAuth()
    else:
        from api.v1.auth.auth import Auth
        auth = Auth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ To handle not found
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def not_authorized(error) -> str:
    """
    Default handler for unauthorized requests.
    """
    return (jsonify({"error": "Unauthorized"}), 401)


@app.errorhandler(403)
def not_allowed(error) -> str:
    """
    Default handler for requests forbidden
    resource.
    """
    return (jsonify({"error": "Forbidden"}), 403)


@app.before_request
def before_request():
    """
    filter out before request
    """
    paths = ["/api/v1/status/",
             "/api/v1/unauthorized/",
             "/api/v1/forbidden/",
             "/api/v1/auth_session/login/"]

    path = request.path

    if auth and auth.require_auth(path, paths):
        # ToCheck for unauthorized requests
        if (not auth.authorization_header(request) and
                not auth.session_cookie(request)):
            abort(401)

        # Retrieve the current authenticated user
        request.current_user = auth.current_user(request)

        # Check for forbidden requests for current user
        if not auth.current_user(request):
            abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)