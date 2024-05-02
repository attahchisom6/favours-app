#!/usr/bin/env python3
"""
This module defines the logic of interacting with the datavase for an
object, if the object is not found in DB we interact with the file storage
for the object
"""
import requests


def deserialize_response(clss, data):
    """
    converts the json representation of an object back to instances
    """
    if not data:
        return None
    if isinstance(data, list):
        return [clss(**obj) for obj in data]
    elif isinstance(data, dict):
        return clss(**data)
    return None

def storage_interactor(url, clss, method, data=None):
    """
    interacts with the datttaaes for rewuired class instances
    """
    if not isinstance(data, dict):
        return "Object must be a dictionary entry"
    try:
        res = requests.request(method, url=url, json=data)
        db_data = res.json()[0]
        if isinstance(db_data, list):
            instance = deserialize_response(clss, db_data[0])
        elif isinstance(db_data, dict):
            instance = deserialize_response(clss, data)
        else:
            instance = None
    except Exception as e:
        print(f"could not find {clss.__name__} objects in DB: {e}")
        instance = None

    if instance is None:
        try:
            instance = clss.search(**data)
            print(f"file object: {instance}")
        except Exception as e:
            print(f"could not fetch {clss.__name__} objects in the file: {e}")

    if instance is None:
        return None

    return instance