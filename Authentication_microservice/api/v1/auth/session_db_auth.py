#!/usr/bin/env python3
"""
This module defines and stores users session to the database
"""
from Authentication_microservice.api.v1.auth.session_db_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user import User


class(SessionExpAuth):
  """
  define the logic/algorithm in which our session_id and user_id are saved
  """
  def create_session(self, user_id: str = None) -> str:
    """
    create session_id and return it, a user_session instance and store in Db
    """
    if user_id is None:
      return None

    user = User.search({"id": user_id})[0]
    if user is None:
      return None

    session_id = super.create_session(user.id)
    if session_id is None:
      return None

    kwargs = {
        "user_id": user.id,
        "session_id": session_id   
      }
    user_session = UserSession(**kwargs)
    user_session.save()

    return session_id


  def user_id_for_session_id(self, session_id: str = None) -> str:
    """
    returns user id for a given session_id
    """
    if session_id is None:
      return None

    if session_id not in self.user_dict_by_session_id:
      return None

    user_data = self.user_dict_by_session_id[session_id]
    user_id = user_data.get("user_id")
    created_at = user_data.get("created_at")
    if self.session_duration is None or created_at is None:
      return user_id

    if self.session_duration + created_at < datetime.utcnow():
      self.user_dict_by_session_id.pop(session_id)

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

    # Note we could have searched with session_id but chose to search
    # with user_id because we want to ensure the session has not expired b3fore being destroyed
    user_id = self.user_for_session_id(session_id)
    if user_id is None:
      return False

    user_session = UserSession.search({"user_id": user_id})[0]
    if user_session is None:
      return False

    try:
      user_session.delete()
      UserSession.save()
    except Exception as e:
      return f"Unable to remove user_session instance {user_session.id} from db: {e}"

    return True
