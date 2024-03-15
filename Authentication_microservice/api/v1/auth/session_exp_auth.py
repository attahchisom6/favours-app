#!/usr/bin/env python3
"""
Manage session expiration auth
"""
from datetime import datetime, timedelta
from Authentication_microservice.api.v1.auth.auth import SessionAuth
from os import getenv

class SessionExpAuth(SessionAuth):
  """
  session expire Auth
  """
  user_dict_by_session_id = {}

  def __init__(self):
    try:
      duration = int(getenv("SESSION_DURATION"))
      self.session_duration = timedelta(seconds=duration)
    except (ValueError, TypeError):
      self.session_duration = None

  def create_session(self, user_id: str) -> str:
    """
    overide the parent method
    """
    session_id = super().create_session(user_id)
    if session_id is not None:
      self.user_dict_by_session_id[session_id] = {
          "user_id": user_id,
          "created_at": datetime.utcnow()
        }
      return session_id
    return None

  def user_id_for_session_id(self, session_id) -> str:
    """
    overload tbe parent methdod
    """
    if session_id is None:
      return None

    if session_id not in self.user_dict_by_session_id:
      return None
    user_id = self.user_dict_by_session_id[session_id].get("user_id")

    if self.session_duration is None:
      return user_id

    created_at = self.user_dict_by_session_id[session_id].get("created_at")
    if created_at is None:
      return user_id

    if created_at + self.session_duration < datetime.utcnow():
      return None
    return user_id
