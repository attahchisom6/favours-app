#!/usr/bin/env python3
"""
entry point of our app to handle all session logic
"""
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
from Authentication_microservice.api.v1.views import app_views
from os import getenv


app = Flask(__name__)


app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
auth_type = getenv("AUTH_TYPE")

if auth_type == "auth":
  from Authentication_microservice.api.v1.auth.auth import Auth
  auth = Auth()
elif auth_type == "bearer_auth":
  from Authentication_microservice.api.v1.auth.bearer_auth import BearerAuth
  auth = BearerAuth()
elif auth_type == "session_auth":
  from Authentication_microservice.api.v1.auth.session_auth import SessionAuth
  auth = SessionAuth()
elif auth_type == "session_exp_auth":
  from Authentication_microservice.api.v1.auth.session_exp_auth import SessionExpAuth
  auth = SessionExpAuth()
elif auth_type == "session_db_auth":
  from Authentication_microservice.api.v1.auth.session_db_auth import SessionDBAuth
  auth = SessionDBAuth()


@app.errorhandler(404)
def not_found(error) -> str:
  """
  customize the not found error
  """
  return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized(error) -> str:
  """
  customize unauthorized error
  """
  return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden_routes(error) -> str:
  """
  customize forbidden route error
  """
  return jsonify({"error": "Forbidden"}), 403

@app.before_request
def manage_authorized_routes():
  """
  handle request before they are parsed
  """
  excluded_paths = [
      "/api/v1/status/",
      "/api/v1/stats/",
      "/api/v1/unauthorized/",
      "/api/v1/forbidden/"
    ]
  if auth is not None and auth.authorized_paths(request.path, excluded_paths) is True:
    if not auth.authorization_header(request) and not auth.session_cookie(request):
      abort(401)

    if not auth.current_user(request):
      abort(403)
    request.current_user = auth.current_user(request)


if __name__ == "__main__":
  host = getenv("HOST", "0.0.0.0")
  port = int(getenv("PORT", "5002"))
  app.run(host=host, port=port, debug=True)
