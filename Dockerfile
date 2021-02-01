FROM python:3.8-buster

RUN apt-get update
RUN apt-get -y install nodejs npm libatlas-base-dev libffi-dev libgl1 usbutils
RUN apt-get clean

RUN npm config set unsafe-perm true

RUN npm install npm@latest -g

RUN node --version && \
    npm --version && \
    python --version && \
    pip --version

WORKDIR /src

COPY requirements.txt .
RUN pip install -r requirements.txt

ADD . .

RUN echo "/src" >> /usr/local/lib/python3.8/site-packages/blocktopus.pth

RUN npm install
RUN ./node_modules/.bin/rollup -c

RUN pip install .

WORKDIR /src
RUN python build.py

WORKDIR /app
COPY start.sh .
RUN ["chmod", "+x", "start.sh"]

# Start the platform
CMD ./start.sh
