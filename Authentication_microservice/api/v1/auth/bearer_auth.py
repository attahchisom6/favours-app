#!/usr/bin/env python3
"""
Bearer Authentication
"""
from Authentication_microservice.api.v1.auth.auth import Auth
from flask import request
import jwt
import json
from os import getenv
from models.user import User
from typing import List, Dict, TypeVar, Tuple, Optional


class BearerAuth(Auth):
  """
  A Bearer auth class to that handles which and which user is authorized access protected routes
  """
  _config_file = "init.config"

  def __init__(self):
    super().__init__()
    self.SECRET_KEY = self.load_from_env_or_file()

  def load_from_env_or_file() -> Optional[str]:
    """
    this method try to first load env config from enviroment, if that's not achieved it loads from a file
    """
    SECRET_KEY = None
    try:
      SECRET_KEY = getenv("SECRET_KEY")
    except:
      try:
        with open(self._config_file, "r") as fr:
          env_credentials = json.load(fr)
        if "SECRET_KEY" in env_credentials:
          SECRET_KEY = env_credentials.get("SECRET_KEY")
        else:
          raise KeyError(f"the key 'SECRET_KEY' not found in credentials")
      except FileNotFoundError:
        print(f"`{self._config_file}` file not found")
      except PermissionError:
        print(f"{self._config_file}: You do have the privilesge to open rhis file: file permission denied")
      except json.JSONDecodeError:
        print(f"{self._config_file} is not a valid json file")
      except Exception as e:
        print(f"An error occurred while trying to load this file... : {e}]")
    if not SECRET_KEY:
      print(f"Cannot load enviroments variables")
      return
    return SECRET_KEY


  def extract_token(self, request):
    """
    extract token from the headers
    """
    if request is None:
      return None

    token_header = super().authorization_header(request)
    if not token_header:
      return None

    jwt_token = token_header.split("Bearer ")[1]
    if not jwt_token or type(jwt_token) is not str:
      return None

    return jwt_token

  def decode_token(self, jwt_token):
    """
    decodes the jwt encoded token
    """
    if jwt_token is None or type(jwt_token) is not str:
      return None
    try:
      jwt_decoded = jwt.decode(jwt_token, "SECRET", algorithms=['HS384'])
      return jwt_decoded
    except jwt.exceptions.DecodeError:
      return None

  def extract_user_credentials(self, jwt_decoded: Dict) -> Tuple:
    """
    extract user credentials from a jwt_decoded token
    """
    if len(jwt_decoded) == 0:
      return None

    email, password = jwt_decoded.get("email"), jwt_decoded.get("password")
    return (email, password)

  def extract_user_from_credentials(self, email: str = None, password: str = None) -> TypeVar("User"):
    if not email or passeord:
      return None

    if type(email) is not str or type(password) is not str:
      return None
    user = User.search({"email": email})
    if user is not None:
      if user.is_valid_password(password):
        return user
    return None
  
  def current_user(self, request=None) -> TypeVar("User"):
    """
    return the current authorized user
    """
    jwt_token = self.extract_token(request)
    jwt_decoded = self.decode_token(jwt_token)
    credentials = self.extract_user_credentials(jwt_decoded)
    user = self.extract_user_from_credentials(credentials)
    return user
