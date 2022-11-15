# Bus path finding app

This project was created during Agents and actors based decision systems course at WUT.

## Requirements and installation
To create and activate [virtual environnement](https://docs.python.org/3/tutorial/venv.html) run:
```
# Create venv
python3 -m venv venv

# Activate venv
source venv/bin/activate
```

Required version of Python is **>=3.8**.

All dependencies needed for the usage of the package are stored in the `requirements.txt` file. To install run:
```
pip install -r requirements.txt
```

In case of development install packages stored in the `requirements-dev.txt` file.

## XMPP server
To start XMPP server go to `containers` directory and run command `docker-compose up`. To stop container hit `ctrl+c` or run command `docker-compose stop` in other terminal (the same directory).

New users are added via `add_agents.sh` script. To execute script run eg. `source add_agents.sh`.

## Agents
### Driver
Agent implementing Driver role.

Internal state:
* geolocation - X and Y coordinates
* current_path - current path for the driver
* capacity - left space (seats) in the driver vehicle

Behaviours:
* ReceiveInformPathChange - changes current path
* ReceiveRequestDriverData - request driver data (state)
* InformDriverData - Inform Manager with a current state

## Tests
To run test execute command:
```
PYTHONPATH=$(pwd) pytest tests
```
`PYTHONPATH` is needed for setting path to `do_celu` package.
