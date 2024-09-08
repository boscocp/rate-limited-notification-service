# Rate-Limited Notification Service
This notification system is designed to redirect email notifications of various types. 
Before each specific type of notification, ensure that the corresponding notification 
type is explicitly included. Additionally, this system rejects requests that exceed 
predefined limits.

Example: POST - http://localhost:5000/time-rule/create
```
{
  "type":"news",
  "limit": 2,
  "time": 120
} 
```
And then: POST - http://localhost:5000/users/notify
```
{
  "email":"bosco@gmail.com",
  "type": "news",
  "message": "Hello World!"
}
```

## API
You can access the documentation at http://localhost:5000/docs

# DynamoDB tables:
In order to define the time rules, this project has two tables: Users and TimeRule.

The Users table is a DynamoDB table with the following structure
| email (PK)       | type (SK) | Attributes |
| ---------------- | --------- | ---------- |
| bosc@gmail.com   | ex. news  | etc.       |

The TimeRule table is a DynamoDB table with the following structure
| type (PK)       | Attributes |
| --------------- | ---------- |
| ex. news        | etc.       |

# To run the project
Using docker compose:
`docker-compose up --build`

# Env configuration
Creating venv using python 3.12:

`python -m venv ./venv`

activating on windows: `venv\Scripts\activate.bat`

on macOS or linux: `source venv/bin/activate`

`pip install -r requirements.txt`

# Env configuration
To execute tests...
`python -m pytest -s`