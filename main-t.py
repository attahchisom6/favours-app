# main_app.py

import requests
from os import getenv

FILE_STORAGE_URL = 'http://file_storage_microservice:5000'
DB_STORAGE_URL = 'http://db_storage_microservice:5000'
STORAGE_TYPE = getenv('HBNB_TYPE_STORAGE')

def get_objects(cls):
    if STORAGE_TYPE == 'file':
        response = requests.get(f'{FILE_STORAGE_URL}/{cls}')
    elif STORAGE_TYPE == 'db':
        response = requests.get(f'{DB_STORAGE_URL}/{cls}')
    return response.json()

if __name__ == '__main__':
    objects = get_objects('User')
    print(objects)

