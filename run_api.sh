#! /bin/bash

# SUPERUSER=""
# SECRET=""
PORT=5000

SUPERUSER=""
SECRET=""
PORT="5000"

# Parse command line arguments
while getopts ":u:s:p:" opt; do
  case ${opt} in
    u ) SUPERUSER=$OPTARG;;
    s ) SECRET=$OPTARG;;
    p ) PORT=$OPTARG;;
    \? ) echo "Usage: $0 [-u superuser name] [-s API secret key] [-p port number, default=5000]" >&2; exit 1;;
  esac
done

# Require superuser
if [ -z "$SUPERUSER" ]; then
  echo "PostgreSQL superuse required. Usage: $0 [-u superuser name] [-s API secret key] [-p port number, default=5000]" >&2
  exit 1
fi

# Inform user secret is insecure
if [ -z "$SECRET" ]; then
  echo "Warning, API secret is an insecure empty string" >&2
fi

echo "Creating chit_chat database and adding chat_dev user"

# Database values
DB_NAME="chit_chat_db"
DB_USER="chat_dev"
DB_PASS="chat_dev"

# Check if database already exists, if not then create it
if [ "$( psql -XtAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'" )" = '1' ]; then
    echo "Database already exists"
    
else
    # Create the database
    sudo -u $SUPERUSER psql -c "CREATE DATABASE $DB_NAME;"
fi

# Check if user already exists, if not then create it
if [ "$( psql -XtAc "SELECT 1 FROM pg_user WHERE pg_user.usename='$DB_USER';" )" = '1' ]; then
    echo "User already exists"
else
  # Create the user and grant access to the database
  sudo -u $SUPERUSER psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';"
  sudo -u $SUPERUSER psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
  echo "chit_chat_db created and user chat_dev granted all privileges"
fi

# Create .env file
DB_URL="postgresql+psycopg2://chat_dev:chat_dev@localhost:5432/chit_chat_db"
cat << EOF > .env
DATABASE_URL=$DB_URL
SECRET_KEY="$SECRET"
EOF
echo "The .env file has been created using supplied secret key"

# Create .flaskenv file
cat << EOF > .flaskenv
FLASK_APP=main:create_app
FLASK_DEBUG=True
FLASK_RUN_PORT=$PORT
EOF
echo "The .flaskenv file has been created"


echo "Creating virtual environment and installing requirements"

# Check if Python is installed
if command -v python3 &>/dev/null; then
  # Check if a folder called 'venv' already exists
  if [ -d ".venv" ]; then
    # Check if the virtual environment is active
    if [[ -n "$VIRTUAL_ENV" ]]; then
      # Get Python version numbers (major.minor)
      vermajor=$(python -c"import sys; print(sys.version_info.major)")
      verminor=$(python -c"import sys; print(sys.version_info.minor)")

      # Check python version number (must be greater that 3.8)
      if [ $vermajor -eq 3 ] && [ $verminor -gt 8 ]; then

        # Prevent pycache files from being created
        export PYTHONDONTWRITEBYTECODE=1 

        # Install the required packages from the requirements file
        pip3 install -r requirements.txt | grep -v 'already satisfied'

        pip install --upgrade pip | grep -v 'already satisfied'

        # Drop any tables
        flask db drop

        # Create tables
        flask db create

        # Run app
        flask run

      else 
        echo "Error: This program needs Python 3.9+ to run, to install check out https://www.python.org/downloads/"
      fi 
    else
      # Activate the virtual environment
      source .venv/bin/activate

      # Prevent pycache files from being created
      export PYTHONDONTWRITEBYTECODE=1 

      # Install the required packages from the requirements file
      pip3 install -r requirements.txt | grep -v 'already satisfied'

      pip install --upgrade pip | grep -v 'already satisfied'

      # Drop any tables
      flask db drop

      # Create tables
      flask db create

      # Run app
      flask run

    fi
  else
    # Create a virtual environment
    python3 -m venv .venv

    # Activate the virtual environment
    source .venv/bin/activate

    # Prevent pycache files from being created
    export PYTHONDONTWRITEBYTECODE=1 

    # Install the required packages from the requirements file
    pip3 install -r requirements.txt | grep -v 'already satisfied'

    pip install --upgrade pip | grep -v 'already satisfied' | grep -v 'already satisfied'
    
    # Drop any tables
    flask db drop

    # Create tables
    flask db create

    # Run app
    flask run

  fi 
else
  # Display an error message if Python is not found
  echo "Error: This program needs Python to run, to install check out https://www.python.org/downloads/"
fi