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
        # Install the required packages from the requirements file
        pip3 install -r requirements.txt | grep -v 'already satisfied'
    
        # Display usage
        echo "To run API use: flask run"

      else 
        echo "Error: This program needs Python 3.9+ to run, to install check out https://www.python.org/downloads/"
      fi 
    else
      # Activate the virtual environment
      source .venv/bin/activate

      # Install the required packages from the requirements file
      pip3 install -r requirements.txt | grep -v 'already satisfied'  
    
      # Display usage
      echo "To run API use: flask run"
    fi
  else
    # Create a virtual environment
    python3 -m venv .venv

    # Activate the virtual environment
    source .venv/bin/activate

    # Install the required packages from the requirements file
    pip3 install -r requirements.txt | grep -v 'already satisfied'
    
    # Display usage
    echo "To run API use: flask run"
  fi 
else
  # Display an error message if Python is not found
  echo "Error: This program needs Python to run, to install check out https://www.python.org/downloads/"
fi