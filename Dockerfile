FROM python:3.8-buster

EXPOSE 80 80
EXPOSE 3000 3000
EXPOSE 5000 5000
EXPOSE 8003 8003

RUN apt-get update
RUN apt-get -y install sqlite3 libsqlite3-dev

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /usr/src/app
COPY . /usr/src/app

# needed for vscode
RUN pip install pylint

RUN pybabel compile -d app/static/translations

ENTRYPOINT ["./gunicorn_server.sh"]

#docker build -t flask-docker .
#docker run -p 8003:8003 flask-docker