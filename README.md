# Tigris MongoDB compatibility and Python FastAPI example

## Introduction

Welcome to this Tigris MongoDB compatibility and Python FastAPI example app. This repo aims to give you a working example of how you can use the power of Tigris MongoDB compatibility with Python to create modern web applications.

## Prerequisites

- [Python 3](https://www.python.org/downloads/)
- A [Tigris Cloud account](https://console.preview.tigrisdata.cloud/signup) or you can [self-host Tigris](https://www.tigrisdata.com/docs/concepts/platform/self-host/)

## Preparing Tigris

1. Create a project in Tigris.
1. Create an application key, and copy the Project Name, Client ID, and Client Secret values.


## Setting up the environment

Activate your Python virtualenv and install dependencies.

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Add an environment variabled named `MONGODB_URL` with the connection string to Tigris. Be sure to replace `{TIGRIS_CLIENT_ID}`, `{TIGRIS_CLIENT_SECRET}`, and `{TIGRIS_PROJECT_NAME}` with your values.

```sh
export MONGODB_URL="mongodb://{TIGRIS_CLIENT_ID}:{TIGRIS_CLIENT_SECRET}@m1k.preview.tigrisdata.cloud:27018/?authMechanism=PLAIN&tls=true"
export TIGRIS_PROJECT_NAME="{TIGRIS_PROJECT_NAME}"
```

## Run the app

Start the app as follows:

```shell
uvicorn app:app --reload
```

## API endpoints

Create a new Game:

```shell
curl --location --request POST 'http://localhost:8000/games' \
--header 'Content-Type: application/json' \
--data-raw '{
   "name": "Fable Anniversary",
   "price": 4.99,
   "category": "Video Game"
}'
```

List Games:

```shell
curl --location --request GET 'http://localhost:8000/games'
```

Get a single Game:

```shell
curl --location --request GET 'http://localhost:8000/games/{_id}'
```

Delete a Game:

```shell
curl --location --request DELETE 'http://localhost:8000/games/{_id}'
```
