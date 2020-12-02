FROM python:3.6.1-alpine

COPY ./app /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD [ "python", "api.py"]