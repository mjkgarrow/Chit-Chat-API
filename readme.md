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



## API endpoints documentation

### Authentication

The authentication API endpoint allows users to log in to the application and obtain a JWT access token that can be used to access protected endpoints.  

#### Endpoint URL

```
POST /api/auth/session
```

**Request JSON Parameters**

| Parameter | Type   | Required | Description                            |
| --------- | ------ | -------- | -------------------------------------- |
| username  | string | Yes      | The user's username, it must be unique |
| password  | string | Yes      | The user's password                    |


**Response**

The response payload will contain a JSON object with the following fields:

| Field    | Type   | Description                                                              |
| -------- | ------ | ------------------------------------------------------------------------ |
| username | string | The user's username                                                      |
| token    | string | A JWT access token that can be used to access other protected endpoints. |


**Example Request**


```json
POST /api/auth/session HTTP/1.1
Host: 127
Content-Type: application/json

{
    "username": "Matt",
    "password": "1234"
}
```


**Example Response**


```json
HTTP/1.1 200 OK
Content-Type: application/json

{
    "access_token":"mF_9.B5f-4.1JqM",
    "token_type":"Bearer",
    "expires_in":3600,
}
```
Error Responses

The authentication API endpoint may return the following error responses:
HTTP Status Code	Error Message	Description
400	Bad Request	One or more required parameters are missing or invalid.
401	Unauthorized	The user's email or password is incorrect.
500	Internal Server Error	An internal server error occurred.
Authentication

The authentication API endpoint does not require authentication. However, the access token obtained from this endpoint will be required to access other protected endpoints.