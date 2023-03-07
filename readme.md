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

### Authentication

The `authentication` endpoint allows users to log in to the application and obtain a JWT access token that can be used to access protected endpoints.

**_Endpoint URL_**

```
POST /auth/session
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

The authentication API endpoint may return the following error responses:

| HTTP Status Code | Error Message | Description                    |
| ---------------- | ------------- | ------------------------------ |
| 401              | Unauthorized  | Incorrect username or password |
		

**Authentication**

The `authentication` endpoint does not require authentication. However, the access token obtained from this endpoint will be required to access other protected endpoints.

### Get users

The `get users` endpoint allows users to view a list of all current users, including the chatrooms they are part.

**_Endpoint URL_**

```
GET /users
```

**Request JSON Parameters**

Not required


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


### Create user

The `create user` endpoint creates a user in the database and provides a JWT access token that can be used to access protected endpoints.

**_Endpoint URL_**

```
POST /users
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
    "email": "beth@email.com",
    "username": "Beth",
    "password": "12345678"
}
```

**Example Response**

```json
HTTP/1.1 200 OK
Content-Type: application/json

{
    "token":"Ld_9.F3f-4.1JqM",
    "token_type":"Bearer",
    "expires_in":3600,
}
```

**Error Responses**

The authentication API endpoint may return the following error responses:

| HTTP Status Code | Error Message | Description              |
| ---------------- | ------------- | ------------------------ |
| 400              | Bad Request   | Email already registered |
		

**Authentication**

The `create user` endpoint does not require authentication. However, the access token obtained from this endpoint will be required to access other protected endpoints.


### Update user

The `update user` endpoint edits the authenticated users information in the database.

**_Endpoint URL_**

```
PUT /users
```

**Request JSON Parameters**

| Parameter | Type   | Required | Domain     | Description                                                      |
| --------- | ------ | -------- | ---------- | ---------------------------------------------------------------- |
| email     | string | Optional | 320 chars  | The user's email, not null, unique, validated for correct format |
| username  | string | Optional | 20 chars   | The user's username, not null                                    |
| password  | string | Optional | 8-20 chars | The user's password, not null                                    |


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
    "email": "beth@email.com",
    "username": "Beth",
    "password": "12345678"
}
```

**Example Response**

```json
HTTP/1.1 200 OK
Content-Type: application/json

{
    "token":"Ld_9.F3f-4.1JqM",
    "token_type":"Bearer",
    "expires_in":3600,
}
```

**Error Responses**

The authentication API endpoint may return the following error responses:

| HTTP Status Code | Error Message | Description              |
| ---------------- | ------------- | ------------------------ |
| 400              | Bad Request   | Email already registered |
		

**Authentication**

The `update user` endpoint does not require authentication. However, the access token obtained from this endpoint will be required to access other protected endpoints.

