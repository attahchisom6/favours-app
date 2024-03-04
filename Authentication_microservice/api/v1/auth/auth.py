#!/usr/bin/env python3
"""
Authorization class
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
  """
  parent Authorization class
  """
  def authorized_paths(self, path: str, excluded_paths: List[str]) -> bool:
    """
    here every path in  excluded path do not need authorization (i.e isers can use the api without anu authorization needed
    Return:
    True -> if authorization is needed for the path
    False -> otherwise
    """
    if path is None:
      return True

    if not excluded_paths:
      return True

    handle_slashed_paths = [path, path + "/"]

    for excluded in excluded_paths:
      if excluded.endswith("*") and path.startswith(excluded[:-1]):
        return False
      if excluded in handle_slashed_paths:
        return False
    return True

  def authorization_header(self, request=None) -> str:
    """
    returns the header if a valid key is provided
    """
    if request is None:
      return None

    dictt_header = request.headers
    key = "Authorization"
    if key not in dictt_header:
      return None
    return dictt_header[key]

  def current_user(self, request=None) -> TypeVar('User'):
    """
    this method will be developed further
    """
    return None

  def session_cookie(self, request=None):
    """
    stores the current user_data in a cookie
    """
    if request is None:
      return None
    SESSION_NAME = getenv("SESSION_NAME")
    if SESSION_NAME is None:
      return None
    return request.cookies.get(SESSION_NAME)
