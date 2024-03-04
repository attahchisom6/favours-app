#!/usr/bin/env python3
"""
user session class
"""
from models.base_model import BaseModel, Base


class UserSession(BaseModel, Base):
  """
  User session and attributes initialized here
  """
  def __init__(self, *args, **kwargs):
    """
    initializing instance attrivutes
    """
    super().__init__(*args, **kwargs)
    self.user_id = kwargs.get("user_id")
    self.session_id = kwargs.get("session_id")
