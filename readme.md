# Chit-Chat API

Chit-Chat is a CRUD RESTful API built with Flask and running on a PostgreSQL database. Chit-Chat allows users to:
- create public or private chatrooms with one or more members
- join or leave a chatroom
- edit the chatroom name (if a member)
- send messages in a chatroom (if a member)
- edit messages in a chatroom (if user created the message)

## Setup

If using Mac, for first time setup run `run_api.sh`. This creates the database, makes a virtual environment, installs requirements and runs the flask API. Use the following flags and arguments:


| Flag | Required | Argument    | Defaul value           | Description                                                                     |
| ---- | -------- | ----------- | ---------------------- | ------------------------------------------------------------------------------- |
| -u   | Yes      | Superuser   | None                   | The PostgreSQL superuser to log in to the `psql` terminal and create a database |
| -s   | Optional | API_secret  | "chit-chat secret key" | A secret key of your choice (this will determine the JWT hashing signature)     |
| -p   | Optional | Port_number | 5000                   | The port to run the local server on                                             |


**_Example:_**

```
./run_api.sh -u postgres -s "super secret key" -p 8000
```

`run_api.sh` can be run again to start the server, though **_WARNING_** it will drop all tables and restart the server.

For other operating systems, or for a manual approach follow these steps:

1. Open the PostgreSQL shell, providing it with a username (the default is `postgres`):
```
sudo -u postgres psql
```
2. Create PostgreSQL database called `chit_chat_db`:
```sql
CREATE DATABASE chit_chat_db;
```
3. Create a PostgreSQL user called `chat_dev` with the password `chat_dev`:
```sql
CREATE USER chat_dev WITH PASSWORD 'chat_dev';
```
4. Grant the user access to the chit_chat_db and then quit the psql shel:
```sql
GRANT ALL PRIVILEGES ON DATABASE chit_chat_db TO chat_dev;
\q
```
5. Navigate to the app src folder and create .env and .flaskenv files with necessary info, change the `SECRET_KEY` to your own choice:
```bash
echo 'DATABASE_URL="postgresql+psycopg2://chat_dev:chat_dev@localhost:5432/chit_chat_db"\nSECRET_KEY="super secret key"' > .env
echo "FLASK_APP=main:create_app\nFLASK_DEBUG=True\nFLASK_RUN_PORT=5000"  > .flaskenv
```
6. Create virtual environment, activate it and install requirements:
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
7. Create tables, seed data, run application:
```
flask db create
flask db seed
flask run
```

Here are the CLI commands to manage the database:

```
flask db drop       # drop tables from db
flask db create     # create tables in db
flask db seed       # seed db with some data
```

If using Mac you can also run the `run_drop_db.sh` script to delete the PostgreSQL database and user from your system, just provide it with a psql superuser argument, eg:

```
./run_drop_db postgres
```
<br>
<br>

## API endpoints documentation

There are 20 endpoints in the Chit-Chat API.

<p style="text-align: center; font-size: 20px; color:white;font-weight:bold;">AUTHENTICATION</p>

### Session

The `session` endpoint allows users to log in to the application and obtain a JWT access token that can be used to access protected endpoints.

**_Endpoint URL_**

```
POST /auth/session/
```

**Request JSON Parameters**

| Parameter | Type   | Required | Domain     | Description                                                      |
| --------- | ------ | -------- | ---------- | ---------------------------------------------------------------- |
| email     | string | Yes      | 320 chars  | The user's email, not null, unique, validated for correct format |
| username  | string | Yes      | 20 chars   | The user's username, not null                                    |
| password  | string | Yes      | 8-20 chars | The user's password, not null                                    |


**Response**

The response payload will contain a JSON with the following fields:

| Field      | Type   | Description                                                             |
| ---------- | ------ | ----------------------------------------------------------------------- |
| token      | string | A JWT access token that can be used to access other protected endpoints |
| token_type | string | The kind of token type, JWT is always 'Bearer'                          |
| expires_in | int    | Seconds until token expires                                             |


**Example Request**


```json
POST /auth/session HTTP/1.1
Host: 127.0.0.1
Port: 5000
Content-Type: application/json

{   
    "email": "matt@email.com",
    "username": "Matt",
    "password": "12345678"
}
```


**Example Response**


```json
HTTP/1.1 200 OK
Content-Type: application/json

{
    "token":"mF_9.B5f-4.1JqM",
    "token_type":"Bearer",
    "expires_in":3600,
}
```

**Error Responses**

The `session` endpoint may return the following error responses:

| HTTP Status Code | Error Message | Description                    |
| ---------------- | ------------- | ------------------------------ |
| 401              | Unauthorised  | Incorrect username or password |
		

**Authentication**

The `session` endpoint does not require authentication. However, the access token obtained from this endpoint will be required to access other protected endpoints.


---
### 

<br>
<p style="text-align: center; font-size: 20px; color:white;font-weight:bold;">USERS</p>

### Get users

The `get users` endpoint allows users to view a list of all current users, including the chatrooms they are part.

**_Endpoint URL_**

```
GET /users/
```

**Request JSON Parameters**

Not required.


**Response**

The response payload will contain a list of JSONs with the following fields:

| Field    | Type   | Description              |
| -------- | ------ | ------------------------ |
| username | string | The username of the user |


**Example Request**


```json
GET /users HTTP/1.1
Host: 127.0.0.1
Port: 5000
```


**Example Response**


```json
HTTP/1.1 200 OK
Content-Type: application/json

[
    {
        "username": "Matt"
    },
    {
        "username": "Beth"
    }
]
```

**Error Responses**

The `get users` endpoint does not return any error responses:
		

**Authentication**

The `get users` endpoint does not require authentication.

### Get user

The `get user` endpoint allows an authenticated user to view their account information, including their username, creation date, and the chats they are in (which include the chat ID, chat name and members of the chat). Must send a valid user_id int in the request url.

**_Endpoint URL_**

```
GET /users/<user_id>
```

**Request JSON Parameters**

Not required.


**Response**

The response payload will contain a JSON with the following fields:

| Field      | Type         | Description                                                                                                      |
| ---------- | ------------ | ---------------------------------------------------------------------------------------------------------------- |
| id         | string       | The ID of the user                                                                                               |
| username   | string       | The username of the user                                                                                         |
| created_at | string       | The local date and time the useraccount was created                                                              |
| chats      | list of dict | List of dicts of the chats the user is a member, in the format `{"id": int, "chat_name": string, "users": list}` |


**Example Request**


```json
GET /users HTTP/1.1
Host: 127.0.0.1
Port: 5000
Authorization: Bearer eyJhbGciOiJIUzI1NiIXVCJ9TJV...r7E20RMHrHDcEfxjoYZgeFONFh7HgQ
```


**Example Response**


```json
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": 49,
    "username": "Matt",
    "created_at": "Wed, 08 Mar 2023 08:37:48 GMT",
    "chats": [
        {
            "id": 25,
            "chat_name": "Close friends",
            "users": [
                "Matt",
                "Beth"
            ]
        }
    ]
}
```

**Error Responses**

The `get users` endpoint may return the following error responses:

| HTTP Status Code | Error Message | Description                      |
| ---------------- | ------------- | -------------------------------- |
| 401              | Unauthorised  | Unauthorised to access that user |
| 401              | Unauthorised  | Invalid user or chat             |
		

**Authentication**

The `get users` endpoint requires a valid JWT access token in the authorisation header.


### Create user

The `create user` endpoint creates a user in the database and provides a JWT access token that can be used to access protected endpoints. A user account is needed to join chats, send messages and interact with the API.

**_Endpoint URL_**

```
POST /users/
```

**Request JSON Parameters**

| Parameter | Type   | Required | Domain     | Description                                                      |
| --------- | ------ | -------- | ---------- | ---------------------------------------------------------------- |
| email     | string | Yes      | 320 chars  | The user's email, not null, unique, validated for correct format |
| username  | string | Yes      | 20 chars   | The user's username, not null                                    |
| password  | string | Yes      | 8-20 chars | The user's password, not null                                    |


**Response**

The response payload will contain a JSON with the following fields:

| Field      | Type   | Description                                                             |
| ---------- | ------ | ----------------------------------------------------------------------- |
| token      | string | A JWT access token that can be used to access other protected endpoints |
| token_type | string | The kind of token type, JWT is always 'Bearer'                          |
| expires_in | int    | Seconds until token expires                                             |


**Example Request**

```json
POST /users/ HTTP/1.1
Host: 127.0.0.1
Port: 5000
Content-Type: application/json

{   
    "email": "beth@email.com",
    "username": "Beth",
    "password": "12345678"
}
```

**Example Response**

```json
HTTP/1.1 201 CREATED
Content-Type: application/json

{
    "token":"Ld_9.F3f-4.1JqM",
    "token_type":"Bearer",
    "expires_in":3600,
}
```

**Error Responses**

The `create user` endpoint may return the following error responses:

| HTTP Status Code | Error Message | Description                                                    |
| ---------------- | ------------- | -------------------------------------------------------------- |
| 400              | Bad Request   | Email already registered                                       |
| 400              | Bad Request   | Incorrect email format                                         |
| 400              | Bad Request   | Username must be at least 1 character                          |
| 400              | Bad Request   | Incorrect password length, must be between 8 and 20 characters |
| 401              | Unauthorised  | Invalid user or chat                                           |
		

**Authentication**

The `create user` endpoint does not require authentication. However, the access token obtained from this endpoint will be required to access other protected endpoints.


### Update user

The `update user` endpoint updates the authenticated user's information in the database with the provided JSON request data.

**_Endpoint URL_**

```
PUT /users/
```

**Request JSON Parameters**

| Parameter | Type   | Required | Domain     | Description                                                      |
| --------- | ------ | -------- | ---------- | ---------------------------------------------------------------- |
| email     | string | Optional | 320 chars  | The user's email, not null, unique, validated for correct format |
| username  | string | Optional | 20 chars   | The user's username, not null                                    |
| password  | string | Optional | 8-20 chars | The user's password, not null                                    |


**Response**

The response payload will contain a JSON with the following fields:

| Field    | Type   | Description                                                                                     |
| -------- | ------ | ----------------------------------------------------------------------------------------------- |
| id       | int    | User's ID                                                                                       |
| email    | string | User's email                                                                                    |
| username | string | User's username                                                                                 |
| password | bool   | Because server doesn't store plaintext passwords, only shows password update status: True/False |


**Example Request**

```json

Original user record:
{   
    "id": 2,
    "email": "beth@email.com",
    "username": "Beth",
    "password": "$2b$12$gV9om/Be2Y.wP3bff8y7jOQx/oARGeQF0GUgEdjmNwhoGnnG9FoXq"
}

PUT /users/ HTTP/1.1
Host: 127.0.0.1
Port: 5000
Authorization: Bearer eyJhbGciOiJIUzI1NiIXVCJ9TJV...r7E20RMHrHDcEfxjoYZgeFONFh7HgQ
Content-Type: application/json

{   
    "email": "fred@email.com",
    "username": "Fred",
}
```

**Example Response**

```json
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": 2,
    "email": "Fred@email.com",
    "username": "Fred",
    "password": "not updated"
}
```

**Error Responses**

The `update user` endpoint may return the following error responses:

| HTTP Status Code | Error Message | Description                                                     |
| ---------------- | ------------- | --------------------------------------------------------------- |
| 400              | Bad Request   | Incorrect email format                                          |
| 400              | Bad Request   | Username must be at least 1 character                           |
| 400              | Bad Request   | Incorrect password length, must be between 8 and 20 characters. |
| 401              | Unauthorised  | Email already registered                                        |
| 401              | Unauthorised  | Invalid user or chat                                            |


**Authentication**

The `update user` endpoint requires a valid JWT access token in the authorisation header.

### Delete user

The `delete user` endpoint removes the authenticated user from all chats, deletes all user-created messages and deletes the user from the database.

**_Endpoint URL_**

```
DELETE /users/
```

**Request JSON Parameters**

Not required.


**Response**

The response payload will contain a JSON with the following fields:

| Field    | Type   | Description                                               |
| -------- | ------ | --------------------------------------------------------- |
| id       | int    | User's ID                                                 |
| username | string | User's username                                           |
| chats    | list   | A list of the names of the chats the user was a member of |


**Example Request**

```json
DELETE /users/ HTTP/1.1
Host: 127.0.0.1
Port: 5000
Authorization: Bearer eyJhbGciOiJIUzI1NiIXVCJ9TJV...r7E20RMHrHDcEfxjoYZgeFONFh7HgQ
```

**Example Response**

```json
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": 1,
    "username": "Matt",
    "chats": [
        "Close friends",
        "Family"
    ]
}
```

**Error Responses**

The `delete user` endpoint may return the following error responses if the user is not correctly authenticated

| HTTP Status Code | Error Message | Description          |
| ---------------- | ------------- | -------------------- |
| 401              | Unauthorised  | Invalid user or chat |
		

**Authentication**

The `delete user` endpoint requires a valid JWT to be provided in the authorisation header.

---
### 

<br>
<p style="text-align: center; font-size: 20px; color:white;font-weight:bold;">CHATS</p>

### Get chats

The `get chats` endpoint allows users to view a list of all available chats and who is the in the chat.

**_Endpoint URL_**

```
GET /chats/
```

**Request JSON Parameters**

Not required.


**Response**

The response payload will contain a list of JSONs with the following fields:

| Field      | Type   | Description                                                     |
| ---------- | ------ | --------------------------------------------------------------- |
| id         | int    | The ID of the chat                                              |
| chat_name  | string | The name of the chat                                            |
| created_at | string | The local  datetime representation of when the chat was created |
| users      | list   | A list of usernames that are members of the chat                |


**Example Request**


```json
GET /chats/ HTTP/1.1
Host: 127.0.0.1
Port: 5000
```


**Example Response**


```json
HTTP/1.1 200 OK
Content-Type: application/json

[
    {
        "id": 1,
        "chat_name": "Close friends",
        "created_at": "March 07, 2023 at 9:19:26 PM",
        "users": [
            "Matt",
            "Beth"
        ]
    }
]
```

**Error Responses**

The `get chats` endpoint does not return any error responses:
		

**Authentication**

The `get chats` endpoint does not require authentication.


### Create chat

The `create chat` endpoint allows an authenticated user to create a public or private chat and add other users to it. To make a public chat, just set the passkey to an empty string, this means anyone can join the chat or view who the members are (private chats don't reveal the members and require the passkey to join). It requires a valid JWT to be submitted in an authorisation header.

**_Endpoint URL_**

```
POST /chats/
```

**Request JSON Parameters**

| Parameter    | Type   | Required | Domain             | Description                                                           |
| ------------ | ------ | -------- | ------------------ | --------------------------------------------------------------------- |
| chat_name    | string | Yes      | 1-20 chars         | The name of the chat, not null                                        |
| chat_passkey | string | Yes      | 0-20 chars         | A secret passkey for the chat, nullable                               |
| users        | list   | Yes      | 0 or more elements | A list of user ID integers that you want to add to the chat, not null |


**Response**

The response payload will contain a JSON with the following fields:

| Field      | Type   | Description                                                     |
| ---------- | ------ | --------------------------------------------------------------- |
| id         | int    | The ID of the chat                                              |
| chat_name  | string | The name of the chat                                            |
| created_at | string | The local  datetime representation of when the chat was created |
| users      | list   | A list of usernames that are members of the chat                |


**Example Request**


```json
GET /chats/ HTTP/1.1
Host: 127.0.0.1
Port: 5000
Authorization: Bearer eyJhbGciOiJIUzI1NiIXVCJ9TJV...r7E20RMHrHDcEfxjoYZgeFONFh7HgQ
Content-Type: application/json

{
    "chat_name": "Close friends",
    "chat_passkey": "1234",
    "users": [1,3,6]
}
```


**Example Response**


```json
HTTP/1.1 201 CREATED
Content-Type: application/json

[
    {
        "id": 1,
        "chat_name": "Close friends",
        "created_at": "March 07, 2023 at 9:19:26 PM",
        "users": [
            "Matt",
            "Beth",
            "Rohan"
        ]
    }
]
```

**Error Responses**

The `create chat` endpoint may return the following error responses:

| HTTP Status Code | Error Message | Description                          |
| ---------------- | ------------- | ------------------------------------ |
| 400              | Bad Request   | Chat name must be 1 to 20 characters |
| 401              | Unauthorised  | Invalid user or chat                 |

		

**Authentication**

The `create chat` endpoint requires a valid JWT to be provided in the authorisation header.


### Get chat passkey

The `get chat passkey` endpoint allows an authenticated user to get the passkey of a chat for which they are a member. Must send a valid chat_id int in the request url.

**_Endpoint URL_**

```
GET /chats/<chat_id>/passkey
```

**Request JSON Parameters**

Not required.


**Response**

The response payload will contain a list of JSONs with the following fields:

| Field        | Type   | Description                                                     |
| ------------ | ------ | --------------------------------------------------------------- |
| chat_passkey | string | The passkey of the requested chat, if empty then chat is public |


**Example Request**


```json
GET /chats/3/passkey HTTP/1.1
Host: 127.0.0.1
Port: 5000
Authorization: Bearer eyJhbGciOiJIUzI1NiIXVCJ9TJV...r7E20RMHrHDcEfxjoYZgeFONFh7HgQ
```


**Example Response**


```json
HTTP/1.1 200 OK
Content-Type: application/json

{
    "chat_passkey": "ciOiJjJ9TZFONFfeFO"
}
```


**Error Responses**


| HTTP Status Code | Error Message | Description          |
| ---------------- | ------------- | -------------------- |
| 401              | Unauthorised  | Invalid user or chat |


**Authentication**

The `get chat passkey` endpoint requires a valid JWT access token in the authorisation header.

### Update chat

The `update chat` endpoint updates the chat name the authenticated user is a member of. Must send a valid chat_id int in the request url.

**_Endpoint URL_**

```
PUT /chats/<chat_id>
```

**Request JSON Parameters**

| Parameter | Type   | Required | Domain     | Description       |
| --------- | ------ | -------- | ---------- | ----------------- |
| chat_name | string | Optional | 1-20 chars | The new chat name |


**Response**

The response payload will contain a JSON with the following fields:

| Field      | Type   | Description                                                                                                                                        |
| ---------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| id         | int    | The chat ID                                                                                                                                        |
| chat_name  | string | The updated chat name                                                                                                                              |
| created_at | string | Local time chat was created                                                                                                                        |
| users      | list   | If chat has no passkey the list contains the usernames of the members, if the chat is protect by a passkey only `Private chat` will be in the list |


**Example Request**

```json

Original user record:
{   
    "id": 2,
    "chat_name": "The old chat name",
    "created_at": "March 08, 2023 at 8:29:31 PM",

}

PUT /chats/2 HTTP/1.1
Host: 127.0.0.1
Port: 5000
Authorization: Bearer eyJhbGciOiJIUzI1NiIXVCJ9TJV...r7E20RMHrHDcEfxjoYZgeFONFh7HgQ
Content-Type: application/json

{   
    "chat_name": "Updated chat name"
}
```

**Example Response**

```json
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": 21,
    "chat_name": "Updated chat name",
    "created_at": "March 08, 2023 at 8:29:31 PM",
    "users": [
        "Private chat"
    ]
}
```

**Error Responses**

The `update chat` endpoint may return the following error responses:

| HTTP Status Code | Error Message | Description                           |
| ---------------- | ------------- | ------------------------------------- |
| 400              | Bad Request   | Chat name must be 1 to 20 characters. |
| 401              | Unauthorised  | Invalid user or chat                  |


**Authentication**

The `update chat` endpoint requires a valid JWT access token in the authorisation header.

### Delete chat

The `delete chat` endpoint removes the authenticated user from all chats, deletes all user-created messages and deletes the user from the database.

**_Endpoint URL_**

```
DELETE /chats/<chat_id>
```

**Request JSON Parameters**

Not required.


**Response**

The response payload will contain a JSON with the following fields:

| Field      | Type   | Description                                                                                                                                        |
| ---------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| id         | int    | The chat ID                                                                                                                                        |
| chat_name  | string | The chat name                                                                                                                                      |
| created_at | string | Local time chat was created                                                                                                                        |
| users      | list   | If chat has no passkey the list contains the usernames of the members, if the chat is protect by a passkey only `Private chat` will be in the list |



**Example Request**

```json
DELETE /chat/5 HTTP/1.1
Host: 127.0.0.1
Port: 5000
Authorization: Bearer eyJhbGciOiJIUzI1NiIXVCJ9TJV...r7E20RMHrHDcEfxjoYZgeFONFh7HgQ
```

**Example Response**

```json
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": 5,
    "chat_name": "Close friends",
    "created_at": "March 08, 2023 at 5:58:31 PM",
    "users": [
        "Private chat"
    ]
}
```

**Error Responses**

The `delete chat` endpoint may return the following error responses if the user is not correctly authenticated

| HTTP Status Code | Error Message | Description          |
| ---------------- | ------------- | -------------------- |
| 401              | Unauthorised  | Invalid user or chat |
		

**Authentication**

The `delete chat` endpoint requires a valid JWT access token in the authorisation header.

---


### Join chat

The `join chat` endpoint adds the authenticated user to the provided valid chat if the provided passkey matches the chat passkey. Must send a valid chat_id int in the request url.

**_Endpoint URL_**

```
PATCH /chats/<chat_id>/join
```

**Request JSON Parameters**

| Parameter    | Type   | Required | Domain     | Description                                        |
| ------------ | ------ | -------- | ---------- | -------------------------------------------------- |
| chat_passkey | string | Optional | 0-20 chars | The passkey of the chat the user is trying to join |

**Response**

The response payload will contain a JSON with the following fields:

| Field         | Type   | Description                            |
| ------------- | ------ | -------------------------------------- |
| id            | int    | The chat ID                            |
| chat_name     | string | The updated chat name                  |
| created_at    | string | Local time chat was created            |
| message_count | int    | The number of messages in the chat     |
| users         | list   | A list of the usernames of the members |


**Example Request**

```json
PATCH /chats/21/join HTTP/1.1
Host: 127.0.0.1
Port: 5000
Authorization: Bearer eyJhbGciOiJIUzI1NiIXVCJ9TJV...r7E20RMHrHDcEfxjoYZgeFONFh7HgQ
Content-Type: application/json

{
    "chat_passkey": "12345"
}
```

**Example Response**

```json
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": 21,
    "chat_name": "Close friends",
    "created_at": "March 08, 2023 at 8:29:31 PM",
    "message_count": 0,
    "users": [
        "Matt",
        "Beth"
    ]
}
```

**Error Responses**

The `join chat` endpoint may return the following error responses:

| HTTP Status Code | Error Message | Description             |
| ---------------- | ------------- | ----------------------- |
| 401              | Unauthorised  | Invalid user or passkey |
| 401              | Unauthorised  | Invalid user or chat    |


**Authentication**

The `join chat` endpoint requires a valid JWT access token in the authorisation header.

---

### Leave chat

The `leave chat` endpoint removes the authenticated user from the provided chat. Must send a valid chat_id int in the request url.

**_Endpoint URL_**

```
PATCH /chats/<chat_id>/leave
```

**Request JSON Parameters**

Not required

**Response**

The response payload will contain a JSON with the following fields:

| Field         | Type   | Description                                                                                                                                        |
| ------------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| id            | int    | The chat ID                                                                                                                                        |
| chat_name     | string | The chat name                                                                                                                                      |
| created_at    | string | Local time chat was created                                                                                                                        |
| message_count | int    | The number of messages in the chat                                                                                                                 |
| users         | list   | If chat has no passkey the list contains the usernames of the members, if the chat is protect by a passkey only `Private chat` will be in the list |


**Example Request**

```json
PATCH /chats/21/leave HTTP/1.1
Host: 127.0.0.1
Port: 5000
Authorization: Bearer eyJhbGciOiJIUzI1NiIXVCJ9TJV...r7E20RMHrHDcEfxjoYZgeFONFh7HgQ
```

**Example Response**

```json
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": 21,
    "chat_name": "Close friends",
    "created_at": "March 08, 2023 at 8:29:31 PM",
    "users": [
        "Private chat"
    ]
}
```

**Error Responses**

The `leave chat` endpoint may return the following error responses:

| HTTP Status Code | Error Message | Description          |
| ---------------- | ------------- | -------------------- |
| 401              | Unauthorised  | Invalid user or chat |


**Authentication**

The `leave chat` endpoint requires a valid JWT access token in the authorisation header.

---



### 

<br>
<p style="text-align: center; font-size: 20px; color:white;font-weight:bold;">MESSAGES</p>

### Get all chat messages

The `get all chat messages` endpoint lists all messages in all a chat where the authenticated user is a member. It requires a valid JWT to be submitted in an authorisation header.

**_Endpoint URL_**

```
GET /messages/chat/<chat_id>
```

**Request JSON Parameters**

Not required.


**Response**

The response payload will contain a list of JSONs, each  with the following fields:

| Field      | Type   | Description                                                                                                                                       |
| ---------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| id         | int    | The message ID                                                                                                                                    |
| message    | string | The message content                                                                                                                               |
| created_at | string | The date the message was sent                                                                                                                     |
| users      | string | The username of the message sender                                                                                                                |
| likes      | dict   | A dict in the form: `{"count": int, "users": list}`, where `count` is the number of likes and `users` is the list of users who liked the message. |


**Example Request**

```json
POST /messages/chat/1 HTTP/1.1
Host: 127.0.0.1
Port: 5000
Authorization: Bearer eyJhbGciOiJIUzI1NiIXVCJ9TJV...r7E20RMHrHDcEfxjoYZgeFONFh7HgQ
```

**Example Response**

```json
HTTP/1.1 200 OK
Content-Type: application/json

[
    {
        "id": 1,
        "message": "Hey! Wazzup?",
        "created_at": "March 09, 2023 at 10:09:01 PM",
        "user": "Matt",
        "likes": {
            "count": 1,
            "users": [
                "Beth",
                "Rohan"
            ]
        }

    },
    {
        "id": 2,
        "message": "Not much dawg",
        "created_at": "March 09, 2023 at 10:09:04 PM",
        "user": "Beth",
        "likes": {}
    }
]
```

**Error Responses**

The `get all chat messages` endpoint may return the following error responses if the user is not correctly authenticated

| HTTP Status Code | Error Message | Description          |
| ---------------- | ------------- | -------------------- |
| 401              | Unauthorised  | Invalid user or chat |
		

**Authentication**

The `get all chat messages` endpoint requires a valid JWT to be provided in the authorisation header.


### Get all user's messages

The `get all user's messages` endpoint lists all the messages sent by the authenticated user. It requires a valid JWT to be submitted in an authorisation header.

**_Endpoint URL_**

```
GET /messages/all_messages/
```

**Request JSON Parameters**

Not required.


**Response**

The response payload will contain a list of JSONs with the following fields:

| Field      | Type   | Description                                                                                                                                       |
| ---------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| id         | int    | The message ID                                                                                                                                    |
| message    | string | The message content                                                                                                                               |
| created_at | string | The date the message was sent                                                                                                                     |
| chat_name  | string | The name of the chat the message was sent in                                                                                                      |
| users      | string | The username of the message sender                                                                                                                |
| likes      | dict   | A dict in the form: `{"count": int, "users": list}`, where `count` is the number of likes and `users` is the list of users who liked the message. |


**Example Request**

```json
POST /messages/latest_messages/ HTTP/1.1
Host: 127.0.0.1
Port: 5000
Authorization: Bearer eyJhbGciOiJIUzI1NiIXVCJ9TJV...r7E20RMHrHDcEfxjoYZgeFONFh7HgQ
```

**Example Response**

```json
HTTP/1.1 200 OK
Content-Type: application/json

[
    {
        "id": 2,
        "message": "See you on the weekend",
        "created_at": "Thu, 09 Mar 2023 11:16:48 PM",
        "chat_name": "Besties",
        "user": "Matt",
        "likes": {
            "count": 1,
            "users": [
                "Beth"
            ]
        }
    }
    {
        "id": 5,
        "message": "Anyone want to have dinner this weekend?",
        "created_at": "Wed, 08 Mar 2023 12:46:12 PM",
        "chat_name": "Family",
        "user": "Matt",
        "likes": {
            "count": 0,
            "users": []
        }
    }
]
```

**Error Responses**

The `get user's latest messages` endpoint may return the following error responses if the user is not correctly authenticated

| HTTP Status Code | Error Message | Description          |
| ---------------- | ------------- | -------------------- |
| 401              | Unauthorised  | Invalid user or chat |
		

**Authentication**

The `get user's latest messages` endpoint requires a valid JWT to be provided in the authorisation header.


### Get user's latest messages

The `get user's latest messages` endpoint lists the lastest message in all the chats where the authenticated user is a member. It requires a valid JWT to be submitted in an authorisation header.

**_Endpoint URL_**

```
GET /messages/latest_messages/
```

**Request JSON Parameters**

Not required.


**Response**

The response payload will contain a list of JSONs with the following fields:

| Field      | Type   | Description                                                                                                                                       |
| ---------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| id         | int    | The message ID                                                                                                                                    |
| message    | string | The message content                                                                                                                               |
| created_at | string | The date the message was sent                                                                                                                     |
| chat_name  | string | The name of the chat the message was sent in                                                                                                      |
| users      | string | The username of the message sender                                                                                                                |
| likes      | dict   | A dict in the form: `{"count": int, "users": list}`, where `count` is the number of likes and `users` is the list of users who liked the message. |


**Example Request**

```json
POST /messages/latest_messages/ HTTP/1.1
Host: 127.0.0.1
Port: 5000
Authorization: Bearer eyJhbGciOiJIUzI1NiIXVCJ9TJV...r7E20RMHrHDcEfxjoYZgeFONFh7HgQ
```

**Example Response**

```json
HTTP/1.1 200 OK
Content-Type: application/json

[
    {
        "id": 2,
        "message": "See you on the weekend",
        "created_at": "Thu, 09 Mar 2023 11:16:48 PM",
        "chat_name": "Besties",
        "user": "Matt",
        "likes": {
            "count": 1,
            "users": [
                "Beth"
            ]
        }
    }
    {
        "id": 6,
        "message": "What are you up to?",
        "created_at": "Wed, 08 Mar 2023 12:46:12 PM",
        "chat_name": "Family",
        "user": "Tim",
        "likes": {
            "count": 0,
            "users": []
        }
    }
]
```

**Error Responses**

The `get user's latest messages` endpoint may return the following error responses if the user is not correctly authenticated

| HTTP Status Code | Error Message | Description          |
| ---------------- | ------------- | -------------------- |
| 401              | Unauthorised  | Invalid user or chat |
		

**Authentication**

The `get user's latest messages` endpoint requires a valid JWT to be provided in the authorisation header.


### Create message

The `create message` endpoint allows an authenticated user to create a message in a chat. It requires a valid JWT to be submitted in an authorisation header.

**_Endpoint URL_**

```
POST /chats/
```

**Request JSON Parameters**

| Parameter | Type   | Required | Domain     | Description         |
| --------- | ------ | -------- | ---------- | ------------------- |
| message   | string | Yes      | 5000 chars | The message content |


**Response**

The response payload will contain a JSON with the following fields:

| Field      | Type   | Description                                                                                                                                       |
| ---------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| id         | int    | The message ID                                                                                                                                    |
| message    | string | The message content                                                                                                                               |
| created_at | string | The date the message was sent                                                                                                                     |
| chat_name  | string | The name of the chat the message was sent in                                                                                                      |
| users      | string | The username of the message sender                                                                                                                |
| likes      | dict   | A dict in the form: `{"count": int, "users": list}`, where `count` is the number of likes and `users` is the list of users who liked the message. |


**Example Request**


```json
GET /chats/ HTTP/1.1
Host: 127.0.0.1
Port: 5000
Authorization: Bearer eyJhbGciOiJIUzI1NiIXVCJ9TJV...r7E20RMHrHDcEfxjoYZgeFONFh7HgQ
Content-Type: application/json

{
    "message": "Hey! Wazzup??"
}
```

**Example Response**

```json
HTTP/1.1 201 CREATED
Content-Type: application/json

{
    "id": 11,
    "message": "Hey! Wazzup??",
    "created_at": "March 09, 2023 at 11:02:15 PM",
    "user": "Matt",
    "chat_name": "Close friends",
    "likes": {
        "count": 0,
        "users": []
    }
}
```

**Error Responses**

The `create message` endpoint may return the following error responses:

| HTTP Status Code | Error Message | Description                                         |
| ---------------- | ------------- | --------------------------------------------------- |
| 400              | Bad Request   | Message is too long, must be under 5000 characters. |
| 401              | Unauthorised  | Invalid user or chat                                |

**Authentication**

The `create message` endpoint requires a valid JWT to be provided in the authorisation header.

### Update message

The `update message` endpoint allows an authenticated user to update the requested message, if they were the creator. It requires a valid JWT to be submitted in an authorisation header.

**_Endpoint URL_**

```
PUT /messages/<message_id>
```

**Request JSON Parameters**

| Parameter | Type   | Required | Domain     | Description                 |
| --------- | ------ | -------- | ---------- | --------------------------- |
| message   | string | Yes      | 5000 chars | The updated message content |


**Response**

The response payload will contain a JSON with the following fields:

| Field      | Type   | Description                                                                                                                                       |
| ---------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| id         | int    | The message ID                                                                                                                                    |
| message    | string | The message content                                                                                                                               |
| created_at | string | The date the message was sent                                                                                                                     |
| chat_name  | string | The name of the chat the message was sent in                                                                                                      |
| users      | string | The username of the message sender                                                                                                                |
| likes      | dict   | A dict in the form: `{"count": int, "users": list}`, where `count` is the number of likes and `users` is the list of users who liked the message. |


**Example Request**


```json
original message:

{
    "id": 11,
    "message": "Hey! Wazzup??",
    "created_at": "March 09, 2023 at 11:02:15 PM",
    "user": "Matt",
    "chat_name": "Close friends",
    "likes": {
        "count": 0,
        "users": []
    }
}

PUT /messages/11 HTTP/1.1
Host: 127.0.0.1
Port: 5000
Authorization: Bearer eyJhbGciOiJIUzI1NiIXVCJ9TJV...r7E20RMHrHDcEfxjoYZgeFONFh7HgQ
Content-Type: application/json

{
    "message": "Hey! What is up??"
}
```

**Example Response**

```json
HTTP/1.1 201 CREATED
Content-Type: application/json

{
    "id": 11,
    "message": "Hey! What is up??",
    "created_at": "March 09, 2023 at 11:02:15 PM",
    "user": "Matt",
    "chat_name": "Close friends",
    "likes": {
        "count": 0,
        "users": []
    }
}
```

**Error Responses**

The `update message` endpoint may return the following error responses:

| HTTP Status Code | Error Message | Description                                         |
| ---------------- | ------------- | --------------------------------------------------- |
| 400              | Bad Request   | Message is too long, must be under 5000 characters. |
| 401              | Unauthorised  | Invalid user or chat                                |

**Authentication**

The `update message` endpoint requires a valid JWT to be provided in the authorisation header.

### Like message

The `like message` endpoint likes or unlikes the requested message - if the user has already liked the message this route will unlike it and vice versa. It requires a valid JWT to be submitted in an authorisation header.

**_Endpoint URL_**

```
DELETE /messages/<message_id>/like
```

**Request JSON Parameters**

Not required.

**Response**

The response payload will contain a JSON with the following fields:

| Field      | Type   | Description                                                                                                                                       |
| ---------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| id         | int    | The message ID                                                                                                                                    |
| message    | string | The message content                                                                                                                               |
| created_at | string | The local time the message was sent                                                                                                               |
| chat_name  | string | The name of the chat the message was sent in                                                                                                      |
| users      | string | The username of the message sender                                                                                                                |
| likes      | dict   | A dict in the form: `{"count": int, "users": list}`, where `count` is the number of likes and `users` is the list of users who liked the message. |

**Example Request**

```json
DELETE /messages/11 HTTP/1.1
Host: 127.0.0.1
Port: 5000
Authorization: Bearer eyJhbGciOiJIUzI1NiIXVCJ9TJV...r7E20RMHrHDcEfxjoYZgeFONFh7HgQ
```

**Example Response**

```json
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": 11,
    "message": "Hey! Wazzup??",
    "created_at": "March 09, 2023 at 11:02:15 PM",
    "user": "Matt",
    "chat_name": "Close friends",
    "likes": {
        "count": 1,
        "users": [
            "Beth"
        ]
    }
}
```

**Error Responses**

The `like message` endpoint may return the following error responses if the user is not correctly authenticated

| HTTP Status Code | Error Message | Description          |
| ---------------- | ------------- | -------------------- |
| 401              | Unauthorised  | Invalid user or chat |
		

**Authentication**

The `like message` endpoint requires a valid JWT access token in the authorisation header.

### Delete message

The `delete message` endpoint deletes the requested message if it was created by the authenticated user. It requires a valid JWT to be submitted in an authorisation header.

**_Endpoint URL_**

```
DELETE /messages/<message_id>
```

**Request JSON Parameters**

Not required.

**Response**

The response payload will contain a JSON with the following fields:

| Field      | Type   | Description                                                                                                                                       |
| ---------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| id         | int    | The message ID                                                                                                                                    |
| message    | string | The message content                                                                                                                               |
| created_at | string | The date the message was sent                                                                                                                     |
| chat_name  | string | The name of the chat the message was sent in                                                                                                      |
| users      | string | The username of the message sender                                                                                                                |
| likes      | dict   | A dict in the form: `{"count": int, "users": list}`, where `count` is the number of likes and `users` is the list of users who liked the message. |

**Example Request**

```json
DELETE /messages/11 HTTP/1.1
Host: 127.0.0.1
Port: 5000
Authorization: Bearer eyJhbGciOiJIUzI1NiIXVCJ9TJV...r7E20RMHrHDcEfxjoYZgeFONFh7HgQ
```

**Example Response**

```json
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": 11,
    "message": "Hey! Wazzup??",
    "created_at": "March 09, 2023 at 11:02:15 PM",
    "user": "Matt",
    "chat_name": "Close friends",
    "likes": {
        "count": 0,
        "users": []
    }
}
```

**Error Responses**

The `delete message` endpoint may return the following error responses if the user is not correctly authenticated

| HTTP Status Code | Error Message | Description          |
| ---------------- | ------------- | -------------------- |
| 401              | Unauthorised  | Invalid user or chat |
		

**Authentication**

The `delete message` endpoint requires a valid JWT access token in the authorisation header.

---

###

