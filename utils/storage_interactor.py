#!/usr/bin/env python3
"""
This module defines the logic of interacting with the datavase for an
object, if the object is not found in DB we interact with the file storage
for the object
"""
import requests
from models.user import User
from models.user_session import UserSession

classes = {
    "User": User,
    "UserSession": UserSession,
}


def deserialize_response(clss, data):
    """
    converts the json representation of an object back to instances
    """
    if not data:
        return None
    if isinstance(data, list):
        return [classes[clss](**obj) for obj in data]
    elif isinstance(data, dict):
        return classes[clss](**data)
    else:
        return None


def storage_interactor(url, clss, method, data=None):
    """
    interacts with the database for required class instances
    """
    if not isinstance(data, dict):
        raise ValueError("Object must be a dictionary entry")
    
    is_file, is_db = False, False
    instances = None

    try:
        res = requests.request(method=method, url=url, json=data)
        if res.status_code == 200:
            db_data = res.json()
            """if isinstance(db_data, list):
                instance = deserialize_response(clss, db_data)[0]
            elif isinstance(db_data, dict):
                instance = deserialize_response(clss, data)
            else:
                instance = None"""
            instances = deserialize_response(clss, db_data)
            if instances:
                is_db = True
                is_file = False
            print(f"db instance: {instances}")
        else:
            print(f"database query returned status code: {res.status_code}")
    except Exception as e:
        print(f"could not find {clss} objects in DB: {e}")
        # instance = None
        raise

    if instances is None:
        try:
            instances = classes[clss].search(data)
            if instances:
                is_db = False
                is_file = True
                print(f"file objects: {instances}")
        except Exception as e:
            print(f"could not fetch {clss} objects in the file: {e}")
            raise

    # if instance is None:
        # return None

    return (instances, is_db, is_file)