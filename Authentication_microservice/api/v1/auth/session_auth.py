                                         #!/usr/bjn/env python3
"""
This modules handles session authentication
"""
from Authentication_microservice.api.v1.auth.auth import Auth
import uuid
from utils.storage_interactor import storage_interactor            


class SessionAuth(Auth):
  """
  session authentication class
  """
  user_id_by_session_id = {}

  def create_session(self, user_id: str = None) -> str:
    """
    create a session id based on the user especialy for caching purposes
    """
    if user_id is None or type(user_id) is not str:
      return None

    session_id = str(uuid.uuid4())
    self.user_id_by_session_id[session_id] = user_id
    return session_id

  def user_id_for_session_id(self, session_id: str) -> str:
    """
    return user based on the session_id
    """
    if session_id is None or type(session_id) is not str:
      return None

    if session_id not in self.user_id_by_session_id:
      return None
    user_id = self.user_id_by_session_id[session_id]
    return user_id

  
  def current_user(self, request=None):
    """
    return the current user from session cookie
    """
    if request is None:
      return None
    
    url = "http://0.0.0.0:5001/search/User"

    session_id = self.session_cookie(request)
    if not session_id:
      return None
    user_id = self.user_id_for_session_id(session_id)
    print(f"user id: {user_id}")
    if not user_id:
      return None
    
    users = storage_interactor(
        url=url,
        clss="User",
        method="POST",
        data={"id": user_id}
    )[0]

    if users is None:
      return None
    user = users[0]
  
    return user.to_dict()


  def destroy_session(self, request) -> bool:
    """
    Destroy a session based on the user id
    """
    flag = True
    if request is None:
      flag = False

    session_id = self.session_cookie(request)
    if session_id is None or session_id not in self.user_id_by_session_id:
      flag = False

    if flag:
      self.user_id_by_session_id.pop(session_id)

    return flag
