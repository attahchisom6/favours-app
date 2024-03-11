#!/usr/bin/env python3
"""
This module defines and stores users session to the database
"""
from Authentication_microservice.api.v1.auth.session_db_auth import SessionExpAuth
from datetime import datetime, timedelta


class(SessionExpAuth):
    """
    define the logic/algorithm in which our session_id and user_id are saved
    """
    def create_session(self, )