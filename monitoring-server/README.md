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
***
# Init system
1. Fill user data [/init_system](http://192.168.0.139:5000/init_system)
2. Fill sample data [/edit-sample](http://192.168.0.139:5000/edit-sample)
3. Init rooms id [/edit-rooms](http://192.168.0.139:5000/edit-rooms)
4. Click button **START** in [/](http://192.168.0.139:5000/)
5. For stop system click button **STOP** in [/](http://192.168.0.139:5000/)