#!/usr/bin/env python3
"""
This module defines and stores users session to the database
"""
from Authentication_microservice.api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime
from models.user_session import UserSession
from utils.storage_interactor import storage_interactor
import requests


class SessionDBAuth(SessionExpAuth):
  """
  define the logic/algorithm in which our session_id and user_id are saved
  """
  def create_session(self, user_id: str = None) -> str:
    """
    create session_id and return it, a user_session instance and store in Db
    """
    if user_id is None:
      return None
    
    url = "http://0.0.0.0:5001/search/User"

    users, is_db, is_file = storage_interactor(
      url=url, clss="User", method="POST",
      data={"id": user_id}
    )

    if users is None or users == []:
      return None
    
    user = users[0]
    session_id = super().create_session(user.id)
    if session_id is None:
      return None

    urll = "http://0.0.0.0:5001/create/UserSession"
    kwargs = {
        "user_id": user.id,
        "session_id": session_id   
      }
    user_session = UserSession(**kwargs)
    if is_file:
      user_session.save()
    elif is_db:
      res = requests.post(urll, json=kwargs)
      if res.status_code == 200:
        print(f"db response {res.json()}")

    return session_id


  def user_id_for_session_id(self, session_id: str = None) -> str:
    """
    returns user id for a given session_id
    """
    if session_id is None:
      return None
    
    url = "http://0.0.0.0:5001/search/UserSession"

    user_sessions, _, _ = storage_interactor(
        url=url,
        clss="UserSession",
        method="POST",
        data={"session_id": session_id}
      )
    if user_sessions is None or user_sessions == []:
      return None
    user_session = user_sessions[0]
    print(f"user_session_here: {user_session}")

    user_id = user_session.user_id
    created_at = user_session.created_at

    if self.session_duration is None or created_at is None:
      return user_id

    if self.session_duration + created_at < datetime.utcnow():
      try:
        user_session.delete()
      except  Exception as e:
        print(f"could not delete use_session object from file: {e}")

      if user_session:
        try:
          res = requests.delete(url=f"http://0.0.0.0:5001/delete/UserSession/{user_session.id}")
          if res.status_code == 200:
            print(res.json())
        except Exception as e:
          print(f"could not delete user_session object from db: {e}")

    return user_id


  def destroy_session(self, request=None) -> bool:
    """
    destroys a user session
    """
    if request is None:
      return False

    session_id = self.session_cookie(request)
    if session_id is None:
      return False

    user_id = self.user_id_for_session_id(session_id)
    if user_id is None:
      return False

    # we search with user_id to ensure the current session has not expired b4 its destroyed
    url = "http://0.0.0.0:5001/search/UserSession"

    user_sessions, is_db, is_file = storage_interactor(
        url=url,
        clss="UserSession",
        method="POST",
        data={"user_id": user_id, "session_id": session_id}
      )
    if user_sessions is None:
      return False
    user_session = user_sessions[0]

    try:
      if is_file:
        user_session.delete()
      elif is_db:
        url = f"http://0.0.0.0:5001/delete/UserSession/{user_session.id}"
        res = requests.delete(url=url)
        if res.status_code == 200:
          print(f"deleting responde: {res.json()}")
      return True     
    except  Exception as e:
      print(f"could not delete use_session object from storage: {e}")
      print(f"is_file: {is_file}, is_db: {is_db}")
      return False
