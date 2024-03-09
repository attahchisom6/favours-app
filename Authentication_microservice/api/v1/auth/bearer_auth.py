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
  _config_file = "config.json"

  def __init__(self):
    super().__init__()
    self.SECRET_KEY = self.load_from_env_or_file()

  def load_from_env_or_file(self) -> Optional[str]:
    """
    this method try to first load env config from enviroment, if that's not achieved it loads from a file
    """
    try:
      secret_key = getenv("SECRET_KEY")
      if secret_key:
        return secret_key
    except EnvironmentError as e:
      print(e)
    try:
      with open(self._config_file, "r") as fr:
        env_credentials = json.load(fr)
        secret_key = env_credentials.get("SECRET_KEY")
        if secret_key:
          return secret_key
        else:
          raise KeyError(f"the key 'SECRET_KEY' not found in credentials")
    except FileNotFoundError:
      print(f"`{self._config_file}` file not found")
    except PermissionError:
      print(f"{self._config_file}: You do have the privilesge to open rhis file: file permission denied")
    except json.JSONDecodeError:
        print(f"{self._config_file} is not a valid json file")
    except Exception as e:
      print(f"An error occurred while trying to load this file...")
    return None


  def extract_token(self, request):
    """
    extract token from the headers
    """
    if request is None:
      return None

    token_header = super().authorization_header(request)
    if not token_header:
      return None

    try:
      jwt_token = token_header.split(" ")[1]
      if token_header.split(" ")[0] != "Bearer":
        return "jwt_token has no Bearer prefix: Error!"
    except IndexError:
      return "Authorization header must have at least 2 units of length"
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
      jwt_decoded = jwt.decode(jwt_token, key=self.SECRET_KEY, algorithms=['HS384'])
      return jwt_decoded
    except jwt.exceptions.DecodeError:
      return None

  def extract_user_credentials(self, jwt_decoded: Dict) -> Tuple:
    """
    extract user credentials from a jwt_decoded token
    """
    if jwt_decoded == None:
      jwt_decoded = {}
    if len(jwt_decoded) == 0:
      return (None, None)

    email, password = jwt_decoded.get("email"), jwt_decoded.get("password")
    return (email, password)

  def extract_user_from_credentials(self, email: str = None, password: str = None) -> TypeVar("User"):
    if not email or not password:
      return None

    if type(email) is not str or type(password) is not str:
      return None
    user = User.search({"email": email})[0]
    if user is not None:
      if user.is_valid_password(password):
        return user.to_dict(fs_indicator=1)
    return None
  
  def current_user(self, request=None) -> TypeVar("User"):
    """
    return the current authorized user
    """
    jwt_token = self.extract_token(request)
    jwt_decoded = self.decode_token(jwt_token)
    credentials = self.extract_user_credentials(jwt_decoded)
    email, password = credentials
    user = self.extract_user_from_credentials(email, password)
    return user
