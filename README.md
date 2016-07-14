# Mont Scrap

Django with React, React-Server, Channels (Websocket and tasks), Scrap

## How to develop

Clone and install requirements
```console
git clone git@github.com:macndesign/mont_scrap.git wttd
cd mont_scrap
python -m venv env
source env/bin/activate
pip install -r requirements.txt
npm install
```

Install Redis Server
```console
# MacOS
homebrew install redis
# Debian
apt-get install redis-server
```

## How to run

Run Webpack
```console
npm run watch
```

Run React Service
```console
npm run react-service
```

Run Redis Server
```
redis-server
```

Run Daphne
```console
daphne mont_scrap.asgi:channel_layer --port 8000
```

Run worker
```console
python manage.py runworker
```
