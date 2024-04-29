#!/usr/bin/env python3
"""
user session class
"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String


class UserSession(BaseModel, Base):
  """
  User session and attributes initialized here
  """
  if models.storage_t == "db":
    __tablename__    = "user_sessions"
    user_id = Column(String(128), nullable=False)
    session_id = Column(String(128), nullable=False)
  else:
    user_id = ""
    session_id = ""

  def __init__(self, *args, **kwargs):
    """
    initializing instance attrivutes
    """
    super().__init__(*args, **kwargs)

