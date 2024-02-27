#!/bin/bash
# command to initiate the db storage with appropraitebenviroment variables

FAVOURS_ENV=db FAVOURS_DB_USER=favour FAVOURS_DB_HOST=localhost FAVOURS_DB_PWD=FAVOURS_PWD FAVOURS_DB_NAME=FAVOURS_DB python3 -m db_storage_microservice.app_db-store
