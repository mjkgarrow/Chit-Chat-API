#! /bin/bash

# Check if superuser roll was supplied
if [ $# -lt 1 ]; then
  echo "Usage: $0 <PostgreSQL superuser role>"
  exit 1
fi

echo "Creating chit_chat database and adding chat_dev user"

# Database values
DB_NAME="chit_chat_db"
DB_USER="chat_dev"
DB_PASS="chat_dev"

# Create the database
sudo -u $1 psql -c "CREATE DATABASE $DB_NAME;"

# Create the user and grant access to the database
sudo -u $1 psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';"
sudo -u $1 psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

echo "chit_chat_db created and user chat_dev granted all privileges"