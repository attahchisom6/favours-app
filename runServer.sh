 #!/usr/bin/bash
 # run each flask server in a tabinated terminal session

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <from_environ_value>"
    exit 1
fi

from_environ="$1"

# Open a new tab for the file storage microservice
gnome-terminal --tab -- python -m file_storage_microservice.app_file_store

# Open a new tab for the database server
gnome-terminal --tab -- ./runDb.sh

# Open a new tab for the authentication microservice with $from_environ obtained from the environment
gnome-terminal --tab -- bash -c "AUTH_TYPE=$from_environ python -m Authentication_microservice.api.v1.app_auth"
