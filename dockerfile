FROM python:alpine3.18

ENV LANG C.UTF-8
WORKDIR /app
RUN apk --no-cache add ffmpeg musl-dev libffi-dev g++ opus-dev
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./commands /app/commands
COPY ./customViews /app/customViews
COPY ./database /app/database
COPY ./enums /app/enums
COPY ./messages /app/messages
COPY ./models /app/models
COPY ./rssreader /app/rssreader
COPY ./utils /app/utils
COPY ./vault /app/vault

WORKDIR /app
COPY ./main.py .
COPY .env .

CMD [ "python3","-OO","main.py" ]