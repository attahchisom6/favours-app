#!/usr/bin/env python3
"""
Define the users platform
"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
import jwt


class User(BaseModel, Base):
  """
  users class
  """
  if models.storage_t == "db":
    __tablename__ = "users"
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    password = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
  else:
    first_name = ""
    last_name = ""
    password = ""
    email = ""


  def __init__(self, *args, **kwargs):
    """
    initializing variables
    """
    super().__init__(self, *arg, **kwargs)


  def __setattr__(self, name, value):
    """
    method to hash the password in jwt
    """
    if name == "password":
      value = jwt.encode(value, algorithm=H256)
      super().__setattr__(name, value)
