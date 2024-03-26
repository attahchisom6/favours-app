#!/usr/bin/env python3
"""
authenticate a user based on the session
"""
from flask import Flask, jsonify, request
from models.user import User
from Authentication_microservice.api.v1.auth.session_auth import SessionAuth
from os import getenv


auth = SessionAuth()

kwargs = {
    "first_name": "Odumeje",
    "last_name": "Peterson",
    "email": "Odumeje@Peterson.com",
    "password": "the brave lion"
}
user = User(**kwargs)
user.save()

user = User.search({"email": kwargs.get("email")})[0]
session_id = auth.create_session(user.id)
init_str = f"the user {user.id} has a session_id {session_id}"

app = Flask(__name__)

@app.route("/current_user", methods=["GET"], strict_slashes=False)
def current_user():
    """
    return the current user
    """
    user  = auth.current_user(request)
    if not user:
        return jsonify({"message": "user not found"}), 404
    return jsonify({"the current_user": user})


if __name__ == "__main__":
    print(init_str)
    app.run(host=getenv("HOST"), port=int(getenv("PORT")), debug=True)