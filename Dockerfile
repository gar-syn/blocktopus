FROM python:3.8-buster

EXPOSE 80 80
EXPOSE 3000 3000
EXPOSE 5000 5000


RUN apt-get update
RUN apt-get -y install sqlite3 libsqlite3-dev


WORKDIR /usr/src/app
# In order for the Docker build cache to cache packages installed via pip,
# it’s necessary to add the requirements.txt file to the image, and run pip install
# before adding the rest of the app code (via COPY . .)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# needed for vscode
RUN pip install pylint

COPY . /usr/src/app
RUN pybabel compile -d app/static/translations
# TODO: implement gunicorn or some other productiongrade server
CMD [ "flask", "run", "--host=0.0.0.0", "--port=5000" ]