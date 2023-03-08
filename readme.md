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

## API endpoints documentation

There are 15 endpoints in the Chit-Chat API:

<br>
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

The `create user` endpoint creates a user in the database and provides a JWT access token that can be used to access protected endpoints.

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

The `create chat` endpoint allows an authenticated user to create a chat and add other users to it. It requires a valid JWT to be submitted in an authorisation header.

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










### Get user's latest messages

The `get user's latest messages` endpoint lists all last message in all the chats where the authenticated user is a member, not including their own. It requires a valid JWT to be submitted in an authorisation header.

**_Endpoint URL_**

```
GET /users/latest_messages/
```

**Request JSON Parameters**

Not required.


**Response**

The response payload will contain a JSON with the following fields:

| Field    | Type          | Description                                                                                   |
| -------- | ------------- | --------------------------------------------------------------------------------------------- |
| id       | int           | User's ID                                                                                     |
| username | string        | User's username                                                                               |
| chats    | list of dicts | A list of chat dictionaries in the form: `{"id": int:chat_id, "chat_name": string:chat name}` |


**Example Request**

```json
POST /auth/session HTTP/1.1
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
        "message": "Not much",
        "user": "Beth",
        "chat_name": "Close friends"
    },
        {
        "id": 4,
        "message": "hey, what's up?",
        "user": "Tim",
        "chat_name": "Close friends"
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

