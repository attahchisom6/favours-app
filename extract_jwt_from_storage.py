#!/usr/bin/env python3
"""
extract a jwt pay load from storage
"""
from models.user import User
import os
from os import getenv
import jwt

keyy = None

def get_jwt_from_payload():
  """
  this function prints a jwt encoding of user credentials
  """
  try:
    user_id = os.environ.get("id")
    if not user_id:
      raise KeyError("No user id provided! pls provide one")
  except KeyError as e:
    return f"Error: {e}"

  try:
    users = User.search({"id": user_id})
    if users is not None:
      user = users[0]
  except Exception as e:
    return f"error reading from the database: {e}"

  email, password = user.email, user.password
  if email and password:
    from Authentication_microservice.api.v1.auth.bearer_auth import BearerAuth
    b = BearerAuth()
    keyy = b.SECRET_KEY
    print(f"SECRET KEY: {keyy}")
    print(f"user: {user.to_dict(fs_indicator=1)}")
    try:
      jwt_encoding = jwt.encode({user.email, }, key=b.SECRET_KEY, algorithm="HS384")
      if jwt_encoding:
        return jwt_encoding
      else:
        return "No encoding"
    except Exception as e:
      return f"encoding failed: {e}"
  else:
    return "neither email nor password can be none"


if __name__ == "__main__":
  jwt_encoding = get_jwt_from_payload()
  print(jwt_encoding)
  print(f"SECRET KEY: {keyy}")
