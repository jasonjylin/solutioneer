# Docker Instructions

## Build the Docker image
`docker build -t fastapi-app .`

## Run the Docker container
`docker run -p 8000:8000 fastapi-app`

## Access on localhost
`localhost:8000`


# Local (no guarantee it will run)

## Requirements
- python3.8
- pip


## Instructions
- run `./setup.sh`
- `source .venv/bin/activate`
- choose to run either the FastAPI server or the cli
- FastAPI: `cd src && python3 app.py` -> `localhost:8000`
- cli: `cd src && python3 cli.py` -> Follow instructions
