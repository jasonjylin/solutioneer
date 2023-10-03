FROM python:3.8

ENV APP_HOST=0.0.0.0
ENV APP_PORT=8000

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install spacy && python3 -m spacy download en_core_web_sm
COPY src /app
COPY .env .env


EXPOSE $APP_PORT

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
