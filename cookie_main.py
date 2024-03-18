#!/usr/bin/env python3
"""
module to test flask cookie
"""
from flask import Flask, jsonify, request
from Authentication_microservice.api.v1.auth.auth import Auth
from os import getenv

auth = Auth()

app = Flask(__name__)

@app.route("/root", methods=["GET"], strict_slashes=False)
def get_cookie():
    """
    returns a cookie value
    """
    session_id = auth.session_cookie(request)
    return jsonify({"the cookie id": session_id})


if __name__ == "__main__":
    app.run(host=getenv("HOST"), port=int(getenv("PORT")), debug=True)