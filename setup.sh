#!/bin/bash

if [ ! -d .venv ]; then
    echo "Creating a Python virtual environment..."
    python -m venv .venv
else
    echo "Python virtual environment already exists."
fi

source .venv/bin/activate

pip install -r requirements.txt

if [ ! -f .env ]; then
    echo "METAPHOR_API_KEY=" > .env
    echo "OPENAI_API_KEY=" >> .env
else
    echo ".env file already exists."
fi

pip install spacy
python -m spacy download en_core_web_sm

