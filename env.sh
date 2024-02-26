#!/usr/bin/bash
# run a simple env command

echo 'create User first_name="first_user" last_name="the user" password="23449" email="first_user@firstuser.com"' | FAVOURS_ENV=db FAVOURS_DB_USER=favour FAVOURS_DB_HOST=localhost FAVOURS_DB_PWD=FAVOURS_PWD FAVOURS_DB_NAME=FAVOURS_DB ./file_console.py

