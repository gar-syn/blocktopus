FROM python:3.8-buster

RUN apt-get update
RUN apt-get -y install nodejs npm libatlas-base-dev dos2unix libffi-dev libgl1
RUN apt-get clean

RUN npm install npm@latest -g

RUN node --version && \
    npm --version && \
    python --version && \
    pip --version

RUN echo "/src/octopus" >> /usr/local/lib/python3.8/site-packages/octopus.pth

WORKDIR /src/octopus
COPY package.json .
RUN npm install

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY twisted/ ./twisted/

COPY rollup.config.js .
COPY octopus/ ./octopus/
RUN ./node_modules/.bin/rollup -c

COPY plugins/ /src/octopus-plugins/
COPY tools/ ./tools/

RUN python tools/install_plugins.py /src/octopus-plugins /usr/local/lib/python3.8/site-packages
RUN python tools/build.py

WORKDIR /app
COPY start.sh .
RUN dos2unix start.sh
RUN ["chmod", "+x", "start.sh"]

# CMD ./start.sh