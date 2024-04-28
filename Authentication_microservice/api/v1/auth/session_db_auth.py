#!/usr/bin/env python3
"""
This module defines and stores users session to the database
"""
from Authentication_microservice.api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user import User
from models.user_session import UserSession
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

    try:
      user = User.search({"id": user_id})[0]
      print(f"file user: {user}")
    except Exception as e:
      print(f"could not find a file user: {e}")
      user = None

    if user is None:
      try:
        from Authentication_microservice.api.v1.views.user_session import deserialize_response
        res = requests.post(url, json={"id": user_id})[0]
        db_data = res.json()
        user = deserialize_response(db_data)
      except Exception as e:
        print(f"could not find a DB user: {e}")

    if user is None:
      return None

    session_id = super.create_session(user.id)
    if session_id is None:
      return None

    url = "http://0.0.0.0:5001/create/UserSession"
    kwargs = {
        "user_id": user.id,
        "session_id": session_id   
      }
    user_session = UserSession(**kwargs)
    try:
      user_session.save()
    except Exception as e:
      print(f"Coudn't save to file: {e}")
    
    try:
      res = requests.post(url, json=kwargs)
      print(res.json())
    except Exception as e:
      print(f"coudn't save to DB")

    return session_id


  def user_id_for_session_id(self, session_id: str = None) -> str:
    """
    returns user id for a given session_id
    """
    if session_id is None:
      return None

    user_session = UserSession.search({"session_id": session_id})[0]
    if not user_session:
      return None

    user_data = user_session.to_dict()
    user_id = user_data["user_id"]
    created_at = user_data["created_at"]

    if self.session_duration is None or created_at is None:
      return user_id

    if self.session_duration + created_at < datetime.utcnow():
      try:
        user_session.delete()
        UserSession.save()
      except:
        return None

    return user_id


  def destroy_session(self, request=None) -> bool:
    """
    destroys a user session
    """
    if request is None:
      return False

    session_id = self.session_cookie(request)
    if session_id:
      return False

    user_id = self.user_id_for_session_id(session_id)
    if user_id is None:
      return False

    # we search with user_id to ensure the current session has not expired b4 its destroyed
    user_session = UserSession.search({"user_id": user_id, "session_id": session_id})[0]
    if user_session is None:
      return False

    try:
      user_session.delete()
      UserSession.save()
    except Exception as e:
      print(f"Unable to remove user_session instance {user_session.id} from db: {e}")
      return False

    return True
