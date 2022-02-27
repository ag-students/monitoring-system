# Run Server
### Activate venv on Ubuntu
```
. venv/bin/activate
```
### Activate venv on Ubuntu with fish
```
. venv/bin/activate.fish
```
### Run flask application
```
export FLASK_APP = monitoring-server.py
export FLASK_ENV = development
flask database clear-db
flask run --host=o.o.o.o
```
