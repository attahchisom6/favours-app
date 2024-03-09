#!/usr/bin/env python3
"""
extract a jwt pay load from storage
"""
from models.user import User
from os import getenv
import jwt

def print_jwt_from_payload():
  """
  this function prints a jwt encoding of user credentials
  """
  try:
    id = getenv("id")
  except EnvironmentError:
    return "provide an id for the user"

  try:
    user = User.search({"id": id})
    if user is not None:
      user = user.to_dict()
  except Exception as e:
    print(f"error reading from the database: {e}")

  email, password = user.email, user.password
  if email and password:
    from Authentication_microservice.api.v1.auth.bearer_auth import BearerAuth
    b = BearerAuth()
    try:
      jwt_encoding = jwt.encode({"email": email, "password": password}, key=b.SECRET_KEY, algorithm="HS384")
      if jwt_encoding:
        print(jwt_encoding)
      else:
        print("No encoding")
    except Exception as e:
      print(f"encoding failed: {e}")
  else:
    print("neither email nor password can be none")
