# Chit-Chat API

Chit-Chat is a CRUD RESTful API built with Flask and running on a PostgreSQL database. Chit-Chat allows users to:
- create chatrooms with one or more members
- join or leave a chatroom
- edit the chatroom name (if a member)
- send messages in a chatroom (if a member)
- edit messages in a chatroom (if user created the message)

## Setup

To create the required PostgreSQL db/db_user run the bash script `run_api.sh`, providing a name of the PostgreSQL superuser to grant access to the psql terminal. This script will also create the db tables:

```
./run_api.sh <Superuser>
```

To activate the Flask server:

```
flask run
```

To drop tables from db:

```
flask db drop
```

To create tables in db:

```
flask db create
```

To seed db with some data:

```
flask db seed
```

## Usage

sdfasdf