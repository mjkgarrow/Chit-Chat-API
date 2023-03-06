#! /bin/bash

# Check if superuser roll was supplied
if [ $# -lt 1 ]; then
  echo "Usage: $0 <PostgreSQL superuser role>"
  exit 1
fi

# Database values
DB_NAME="chit_chat_db"
DB_USER="chat_dev"

# Check if database exists
if [ "$( psql -XtAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'" )" = '1' ]
then
    # Check if user exists
    if [ "$( psql -XtAc "SELECT 1 FROM pg_user WHERE pg_user.usename='$DB_USER';" )" = '1' ]
    then
        echo "Droppping chit_chat database chat_dev user"
        # Drop the database
        sudo -u $1 psql -c "DROP DATABASE $DB_NAME;"

        # DROP the user
        sudo -u $1 psql -c "DROP USER $DB_USER;"

        echo "chit_chat_db created and user chat_dev granted all privileges"

        exit 1
    else
        echo "User doesn't exist"
        exit 1
    fi
else
    echo "Database does not exist"
    exit 1
fi


